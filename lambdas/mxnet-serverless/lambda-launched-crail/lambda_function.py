'''
Reference code to showcase MXNet model prediction on AWS Lambda 

@author: Sunil Mallya (smallya@amazon.com)
version: 0.2
'''

import os
import boto3
import botocore
import json
# import tempfile
import urllib2 
from urllib import urlretrieve
import struct
import sys
from timeit import default_timer as now
import HTMLParser
html_parser = HTMLParser.HTMLParser()

import numpy as np
import mxnet as mx
import subprocess

from PIL import Image
from io import BytesIO
import base64
from collections import namedtuple
from collections import OrderedDict
import os.path
import math
import time
import ifcfg
import threading
import crail
from random import randint
#import psutil

Batch = namedtuple('Batch', ['data'])

f_params = 'resnet-18-0000.params'
f_symbol = 'resnet-18-symbol.json'
LOCAL_IMG_PATH = os.path.join('/tmp', 'local.jpg')
DEFAULT_OUT_FOLDER = 'mxnet-results/'


INPUT_BUCKET = 'video-lambda-input'
OUTPUT_BUCKET = 'video-lambda-input'
    
LOGS_NET_BUCKET= 'video-lambda-logs'
LOGS_BUCKET= 'video-lambda-logs-mxnet'
LOGS_PATH = 'video-lambda-logs-mxnet'


class TimeLog:
  def __init__(self, enabled=True):
    self.enabled = enabled
    self.start = time.time()
    self.prev = self.start
    self.points = []
    self.sizes = []

  def add_point(self, title):
    if not self.enabled:
      return

    now = time.time()
    self.points += [(title, now - self.prev)]
    self.prev = now
    

def get_net_bytes(rxbytes, txbytes, rxbytes_per_s, txbytes_per_s): #, cpu_util):
  SAMPLE_INTERVAL = 1.0
  threading.Timer(SAMPLE_INTERVAL, get_net_bytes, [rxbytes, txbytes, rxbytes_per_s, txbytes_per_s]).start() # schedule the function to execute every SAMPLE_INTERVAL seconds
  #threading.Timer(SAMPLE_INTERVAL, get_net_bytes, [rxbytes, txbytes, rxbytes_per_s, txbytes_per_s, cpu_util]).start() # schedule the function to execute every SAMPLE_INTERVAL seconds
  rxbytes.append(int(ifcfg.default_interface()['rxbytes']))
  txbytes.append(int(ifcfg.default_interface()['txbytes']))
  rxbytes_per_s.append((rxbytes[-1] - rxbytes[-2])/SAMPLE_INTERVAL)
  txbytes_per_s.append((txbytes[-1] - txbytes[-2])/SAMPLE_INTERVAL)
  #util = psutil.cpu_percent(interval=1.0)
  #cpu_util.append(util)

def upload_timelog(socket, ticket, timelogger, reqid):
  logfile = LOGS_PATH + '/mxnet' + reqid
  f = open("/tmp/localLogs", "wb").write(str({'lambda': reqid,
             'started': timelogger.start,
             'timelog': timelogger.points}).encode('utf-8'))
  crail.put(socket, "/tmp/localLogs", logfile, ticket) 
  print "wrote timelog"
  return

def upload_net_bytes(socket, ticket, rxbytes_per_s, txbytes_per_s, cpu_util, timelogger, reqid):
  netstats = LOGS_PATH + '/netstats-mxnet' + reqid 
  f = open("/tmp/localByteStats", "wb").write(str({'lambda': reqid,
             'started': timelogger.start,
             'rx': rxbytes_per_s,
             'tx': txbytes_per_s,
             'cpu': cpu_util}).encode('utf-8'))
  crail.put(socket, "/tmp/localByteStats", netstats, ticket)
  print "wrote netstats"
  return

#params
# start = now()
f_params_file = '/tmp/' + f_params
#urlretrieve("https://s3-us-west-2.amazonaws.com/mxnet-params/resnet-18-0000.params", f_params_file)

#symbol
f_symbol_file = '/tmp/' + f_symbol
#f_symbol_file = '/var/task/' + f_symbol
# urlretrieve("https://s3-us-west-2.amazonaws.com/mxnet-params/resnet-18-symbol.json", f_symbol_file)
# end = now()
# print('Time to download MXNet model: {:.4f} s'.format(end - start))

def ensure_clean_state():
  if os.path.exists(LOCAL_IMG_PATH):
    os.remove(LOCAL_IMG_PATH)

def download_input_from_crail(socket, ticket, fileName, localfile=LOCAL_IMG_PATH):
  obj = crail.get(socket, fileName, localfile, ticket)
  

def upload_output_to_crail(socket, ticket, fileName, out):
  try:
    f = open('/tmp/data.txt', 'wb').write(out)
    crail.put(socket, '/tmp/data.txt', fileName, ticket)
    #s3.put_object(Body=json.dumps(out), Bucket=bucketName, Key=fileName, 
    #              StorageClass='REDUCED_REDUNDANCY')
  except botocore.exceptions.ClientError as e:
    print e
    raise

def one_file_to_many(inPath):
  data = []
  with open(inPath, 'rb') as ifs:
    count = 0
    while True:
      chunk = ifs.read(4)
      if chunk == '':
        break
      fileNameLen = struct.unpack('I', chunk)[0]
      fileName = ifs.read(fileNameLen)
      chunk = ifs.read(4)
      if chunk == '':
        raise Exception('Expected 4 bytes')
      dataLen = struct.unpack('I', chunk)[0]
      data.append(ifs.read(dataLen))
      count += 1
    print('Extracted {:d} files'.format(count))
  return data

    
def load_model(s_fname, p_fname):
  """
  Load model checkpoint from file.
  :return: (arg_params, aux_params)
  arg_params : dict of str to NDArray
      Model parameter, dict of name to NDArray of net's weights.
  aux_params : dict of str to NDArray
      Model parameter, dict of name to NDArray of net's auxiliary states.
  """
  symbol = mx.symbol.load(s_fname)
  save_dict = mx.nd.load(p_fname)
  arg_params = {}
  aux_params = {}
  for k, v in save_dict.items():
    tp, name = k.split(':', 1)
    if tp == 'arg':
      arg_params[name] = v
    if tp == 'aux':
      aux_params[name] = v
  return symbol, arg_params, aux_params

def predict_batch(batch_size, data, mod):
  '''
  predict labels for a given batch of images
  '''
  data_size = len(data)
  cnt = 0
  new_width, new_height = 224, 224
  out = "{"
  while cnt < data_size:
    # execute one batch
    img_list = []
    for frame in data[cnt:cnt+batch_size]:
      img = Image.open(BytesIO(frame))
      width, height = img.size   # Get dimensions
      left = (width - new_width)/2
      top = (height - new_height)/2
      right = (width + new_width)/2
      bottom = (height + new_height)/2

      img = img.crop((left, top, right, bottom))
      # convert to numpy.ndarray
      sample = np.asarray(img)
      # swap axes to make image from (224, 224, 3) to (3, 224, 224)
      sample = np.swapaxes(sample, 0, 2)
      img = np.swapaxes(sample, 1, 2)
      img_list.append(img)

    batch = mx.io.DataBatch([mx.nd.array(img_list)], [])
    mod.forward(batch)
    probs = mod.get_outputs()[0].asnumpy()
    print probs.shape

    cnt_local = cnt
    # the output format is : first is the relative id of the frame
    # then the second.first is the category (num), second.second is the
    # probability / confidence of the category
    # Be aware that this is different from previous version!
    for prob in probs:
      prob = np.squeeze(prob)
      a = np.argsort(prob)[::-1]
      if cnt_local == 0:
        out += '"0" : {{"{}" : "{}"}}'.format(a[0], prob[a[0]])
      else:
        out += ', "{:d}" : {{"{}" : "{}"}}'.format(cnt_local, 
                                                      a[0], prob[a[0]])
      cnt_local += 1

    cnt += batch_size

  out += "}"
  return out

def lambda_s3_batch_handler(event, context):
  #crail.launch_dispatcher(CRAIL_HOME_PATH)
  print("Start lambda handler...")
  p = crail.launch_dispatcher_from_lambda()
  ticket = randint(1,30000)
  timelist = OrderedDict()
  timelogger = TimeLog(enabled=True)
 
  socket = crail.connect()

  crail.create_dir(socket, 'mxnet-results', ticket)
  #crail.create_dir(socket, LOGS_BUCKET, ticket)

  ensure_clean_state()
  inputBucket = INPUT_BUCKET #'vass-video-samples2'
  inputKey = 'batch-test/1901+100.jpg'
  batchSize = 50 # the batch passed to MXNet, cannot be passed through s3 event
  outputBucket = OUTPUT_BUCKET # 'vass-video-samples2-results'
  outputKey = 'mxnet-results/1901-100.out'

  # timelist = "{"
  start = now()
  urlretrieve("https://s3-us-west-2.amazonaws.com/mxnet-params/resnet-18-0000.params", f_params_file)
  #obj = crail.get(socket, "resnet-18-0000.params", f_params_file, ticket)
  urlretrieve("https://s3-us-west-2.amazonaws.com/mxnet-params/resnet-18-symbol.json", f_symbol_file)
  end = now()
  print('Time to download MXNet model: {:.4f} s'.format(end - start))
  # timelist += '"download-model" : %f,' % (end - start)
  timelist["download-model"] = end - start
  timelogger.add_point("download model")


  iface = ifcfg.default_interface()
  rxbytes = [int(iface['rxbytes'])]
  txbytes = [int(iface['txbytes'])]
  rxbytes_per_s = []
  txbytes_per_s = []
  cpu_util = []
  #get_net_bytes(rxbytes, txbytes, rxbytes_per_s, txbytes_per_s)  
  #get_net_bytes(rxbytes, txbytes, rxbytes_per_s, txbytes_per_s, cpu_util)  

  
  inputBucket = OUTPUT_BUCKET #html_parser.unescape(record['s3']['bucket']['name'])
  inputKey = str(event['b64Img']) #html_parser.unescape(record['s3']['object']['key'])
  lambdaID = "parentLambda" + str(event['parentID']) + "-childLambda" + str(event['lambdaID'])
  outputBucket = inputBucket + "-results"
  # outputKey = inputKey.split(".")[0].split("/")[-1] + '.out'
  tmpKeyList = inputKey.split(".")[0].split("/")[-2:]
  direxample = str(DEFAULT_OUT_FOLDER + "/" + tmpKeyList[0])
  print direxample
  crail.create_dir(socket, direxample, ticket)
  outputKey = str(DEFAULT_OUT_FOLDER + '/'.join(tmpKeyList) + '.out')
  print('Outputkey is: {}'.format(outputKey))
  print('Inputkey is: {}'.format(inputKey))

  start = now()
  download_input_from_crail(socket, ticket, inputKey, LOCAL_IMG_PATH)
  end = now()
  timelogger.add_point("download_inputs")
  inputSize = os.path.getsize(LOCAL_IMG_PATH)
  print('Time to download input file: {:.4f} s, size {} KB'.format(
    end - start, inputSize))
  # timelist += '"download-input" : %f,' % (end - start)
  timelist["download-input"] = end - start

  start = now()
  data = one_file_to_many(LOCAL_IMG_PATH)
  end = now()
  count = len(data)
  print('Time to extract {:d} file: {:.4f} s'.format(count, end - start))
  # timelist += '"extract-input" : %f,' % (end - start)
  timelist["extract-input"] = end - start
  if (count % batchSize) != 0:
    print('input files number {:d} cannot be divided by '.format(count) +  
        'batch size {:d}'.format(batchSize))
    # exit()
    if count < 100:
      batchSize = count
    else:
      batchSize = 1
    print('Using batch size: {:d}'.format(batchSize))

  start = now()
  sym, arg_params, aux_params = load_model(f_symbol_file, f_params_file)
  mod = mx.mod.Module(symbol=sym, label_names=None)
  mod.bind(for_training=False, data_shapes=[('data', (batchSize,3,224,224))],
          label_shapes=mod._label_shapes)
  mod.set_params(arg_params, aux_params, allow_missing=True)
  end = now()
  print('Time to prepare and load parameters: {:.4f} s'.format(end - start))
  # timelist += '"load-model" : %f,' % (end - start)
  timelist["load-model"] = end - start
 
  start = now()
  labels = predict_batch(batchSize, data, mod)
  end = now()
  timelogger.add_point("compute")
  print('Time to predict the {:d} batch: {:.4f} s'.format(batchSize, end -
     start))
  # timelist += '"predict" : %f,' % (end - start)
  timelist["predict"] = end - start
  
  start = now()
  #out = {
  #    "results": labels
  #}
  out = labels
  upload_output_to_crail(socket, ticket, outputKey, out)
  end = now()
  timelogger.add_point("upload results")

  print('Time to upload to redis is: {:.4f} s'.format(end - start))
  # timelist += '"upload-output" : %f,' % (end - start)
  timelist["upload-output"] = end - start
  # timelist += '"batch" : %d' % (batchSize)
  timelist["batch"] = batchSize
  # timelist += "}"
  
  upload_timelog(socket, ticket, timelogger, lambdaID) 
  upload_net_bytes(socket, ticket, rxbytes_per_s, txbytes_per_s, cpu_util, timelogger, lambdaID)
  crail.close(socket, ticket, p)
  print 'Timelist:' + json.dumps(timelist)

#if __name__ == '__main__':
  #CRAIL_HOME_PATH = os.environ('CRAIL_HOME')
  #p = crail.launch_dispatcher(CRAIL_HOME_PATH)
  #lambda_s3_batch_handler("", "");
# for local test
#if __name__ == '__main__':
