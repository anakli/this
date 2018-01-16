import os
import sys
import shutil
import subprocess
from multiprocessing.pool import ThreadPool
from threading import Semaphore
import urllib2
from urllib import urlretrieve
from timeit import default_timer as now
import json
from collections import OrderedDict
import math
import time
import crail
import ifcfg
import threading
from random import randint

import os.path

DECODER_PATH = '/tmp/FusedDecodeHist-static'
TEMP_OUTPUT_DIR = '/tmp/output'
LOCAL_INPUT_DIR = '/tmp/input'
WORK_PACKET_SIZE = 50

DEFAULT_LOG_LEVEL = 'warning'

DEFAULT_OUTPUT_BATCH_SIZE = 1
DEFAULT_KEEP_OUTPUT = False

MAX_PARALLEL_UPLOADS = 20

DEFAULT_OUT_FOLDER = 'fused-decode-hist-output'

OUTPUT_FILE_EXT = 'out'

LOGS_PATH = 'video-lambda-logs'



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
    

def get_net_bytes(rxbytes, txbytes, rxbytes_per_s, txbytes_per_s):
  SAMPLE_INTERVAL = 1.0
  threading.Timer(SAMPLE_INTERVAL, get_net_bytes, [rxbytes, txbytes, rxbytes_per_s, txbytes_per_s]).start() # schedule the function to execute every SAMPLE_INTERVAL seconds
  rxbytes.append(int(ifcfg.default_interface()['rxbytes']))
  txbytes.append(int(ifcfg.default_interface()['txbytes']))
  rxbytes_per_s.append((rxbytes[-1] - rxbytes[-2])/SAMPLE_INTERVAL)
  txbytes_per_s.append((txbytes[-1] - txbytes[-2])/SAMPLE_INTERVAL)

def list_output_files():
  fileExt = '.{0}'.format(OUTPUT_FILE_EXT)
  outputFiles = [
    x for x in os.listdir(TEMP_OUTPUT_DIR) if x.endswith(fileExt)
  ]
  return outputFiles

def download_input_from_crail(socket, ticket, inputPrefix, startFrame):
  protoFileName = 'decode_args{:d}.proto'.format(startFrame)
  binFileName = 'start_frame{:d}.bin'.format(startFrame)
  print('Downloading files {:s} and {:s} for batch {:d} \
        from Redis: {:s}'.format(protoFileName, binFileName, startFrame, inputPrefix))
  ProtoName = inputPrefix + '/' + protoFileName
  BinName = inputPrefix + '/' + binFileName
  protoPath = LOCAL_INPUT_DIR + '/' + protoFileName
  binPath = LOCAL_INPUT_DIR + '/' + binFileName

  crail.get(socket, ProtoName, protoPath, ticket) 
  crail.get(socket, BinName, binPath, ticket) 
  
  return protoPath, binPath

def upload_timelog(socket, ticket, timelogger, reqid):
  logfile = LOGS_PATH + '/' + reqid
  f = open.("localLogs", "wb").write(str({'lambda': reqid,
             'started': timelogger.start,
             'timelog': timelogger.points}).encode('utf-8')
  crail.put(socket, "localLogs", logfile, ticket) 
  print "wrote timelog"
  return

def upload_net_bytes(socket, ticket, rxbytes_per_s, txbytes_per_s, timelogger, reqid):
  netstats = LOGS_PATH + '/netstats-' + reqid 
  f = open.("localByteStats", "wb").write(str({'lambda': reqid,
             'started': timelogger.start,
             'rx': rxbytes_per_s,
             'tx': txbytes_per_s}).encode('utf-8')
  crail.put(socket, "localByteStats", netstats, ticket)
  print "wrote netstats"
  return
  

def upload_output_to_crail(socket, ticket, filePrefix):
  print('Uploading files to Redis: {:s}/{:s}'.format(bucketName, filePrefix))

  outputFiles = list_output_files()
  assert(len(outputFiles) == 1) # only one output file!
  fileName = outputFiles[0]
  localFilePath = os.path.join(TEMP_OUTPUT_DIR, fileName)
  uploadFileName = os.path.join(filePrefix, fileName)
  fileSize = os.path.getsize(localFilePath)
  crail.put(socket, localFilePath, uploadFileName, ticket)
  print('Done: [total={:d}KB]'.format(fileSize >> 10))
  fileCount = int(fileName.split('-')[-1].split('.')[0])
  return (fileCount, fileSize)


def ensure_clean_state(socket, ticket):
  if os.path.exists(TEMP_OUTPUT_DIR):
    shutil.rmtree(TEMP_OUTPUT_DIR)
  if not os.path.exists(TEMP_OUTPUT_DIR):
    os.mkdir(TEMP_OUTPUT_DIR)
  if os.path.exists(LOCAL_INPUT_DIR):
    shutil.rmtree(LOCAL_INPUT_DIR)
  if not os.path.exists(LOCAL_INPUT_DIR):
    os.mkdir(LOCAL_INPUT_DIR)

  if os.path.exists(DECODER_PATH):
    os.remove(DECODER_PATH)
  # store decoder binary in redis too
  #urlretrieve("https://s3-us-west-2.amazonaws.com/mxnet-params/FusedDecodeHist-static", DECODER_PATH)
  crail.get(socket, "FusedDecodeHist-static", DECODER_PATH, ticket)
  os.chmod(DECODER_PATH, 0o755)
  

def convert_to_output(protoPath, binPath):
  assert(os.path.exists(TEMP_OUTPUT_DIR))
  cmd = [DECODER_PATH, protoPath, binPath, TEMP_OUTPUT_DIR]
  process = subprocess.Popen(
    ' '.join(cmd), shell=True,
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE)
  out, err = process.communicate()
  rc = process.returncode
  print 'stdout:', out
  print 'stderr:', err
  return rc == 0


def handler(event, context):
  crail.launch_dispatcher()
  timelist = OrderedDict()
  timelogger = TimeLog(enabled=True)

  iface = ifcfg.default_interface()
  rxbytes = [int(iface['rxbytes'])]
  txbytes = [int(iface['txbytes'])]
  rxbytes_per_s = []
  txbytes_per_s = []
  get_net_bytes(rxbytes, txbytes, rxbytes_per_s, txbytes_per_s)  
  
  #TODO: add new timelog entry for connection setup
  time.sleep(1)
  ticket = randint(1,10000)
  socket = crail.connect()  
 
  start = now()
  ensure_clean_state(socket, ticket)
  end = now()
  timelogger.add_point("prepare decoder")
  print('Time to prepare decoder: {:.4f} s'.format(end - start))
  timelist["prepare-decoder"] = (end - start)

  inputBucket = 'vass-video-samples2'
  inputPrefix = 'protobin/example3_134'
  startFrame = 0
  outputBatchSize = 50

  outputBucket = "vass-video-samples2-results"
  outputPrefix = DEFAULT_OUT_FOLDER
  
  if 'inputBucket' in event:
    inputBucket = event['inputBucket']
    outputBucket = inputBucket + '-results'
  else:
    print('Warning: using default input bucket: {:s}'.format(inputBucket))
  if 'inputPrefix' in event:
    inputPrefix = event['inputPrefix']
  else:
    print('Warning: using default input prefix: {:s}'.format(inputPrefix))
  if 'startFrame' in event:
    startFrame = event['startFrame']
  else:
    print('Warning: default startFrame: {:d}'.format(startFrame))
  if 'outputBatchSize' in event:
    outputBatchSize = event['outputBatchSize']
  else:
    print('Warning: default batch size: {:d}'.format(outputBatchSize))
  if 'outputPrefix' in event:
    outputPrefix = event['outputPrefix']

  outputPrefix = outputPrefix + '/{}_{}'.format(inputPrefix.split('/')[-1], 
                                                outputBatchSize)

  start = now()
  protoPath, binPath = download_input_from_crail(socket, ticket, inputPrefix, 
                                              startFrame)
  end = now()
  timelogger.add_point("download_inputs")
  print('Time to download input files: {:.4f} s'.format(end - start))
  timelist["download-input"] = (end - start)

  inputBatch = 0
  try:
    try:
      start = now()
      if not convert_to_output(protoPath, binPath):
        raise Exception('Failed to process video chunk {:d}'.format(startFrame))
      end = now()
      timelogger.add_point("decode and compute hist")
      print('Time to decode and compute hist: {:.4f} '.format(end - start))
      timelist["decode-hist"] = (end - start)
    finally:
      shutil.rmtree(LOCAL_INPUT_DIR)

    # start = now()
    # if outputBatchSize > 1:
    #   inputBatch = combine_output_files(startFrame, outputBatchSize)
    # end = now()
    # print('Time to combine output files: {:.4f} '.format(end - start))
    # timelist["combine-output"] = (end - start)

    start = now()
    fileCount, totalSize = upload_output_to_crail(socket, ticket, outputPrefix)
    end = now()
    outputBatchSize = fileCount
    timelogger.add_point("upload output")
    print('Time to upload output files: {:.4f} '.format(end - start))
    timelist["upload-output"] = (end - start)

  finally:
    start = now()
    if not DEFAULT_KEEP_OUTPUT:
      shutil.rmtree(TEMP_OUTPUT_DIR)
    end = now()
    timelogger.add_point("clean output")
    print('Time to clean output files: {:.4f} '.format(end - start))
    timelist["clean-output"] = (end - start)
  
  timelist["output-batch"] = outputBatchSize

  upload_timelog(socket, timelogger, context.aws_request_id) 
  upload_net_bytes(socket, rxbytes_per_s, txbytes_per_s, timelogger, context.aws_request_id)

  print 'Timelist:' + json.dumps(timelist)
  out = {
    'statusCode': 200,
    'body': {
      'startFrame': startFrame,
      'outputBatchSize': outputBatchSize
    }
  }
  return out


if __name__ == '__main__':
  inputBucket = 'vass-video-samples2'
  inputPrefix = 'protobin-fused-local/example3_138_50'
  startFrame = 0
  outputBatchSize = 50
  outputPrefix = 'fused-decode-hist-local'
  totalFrame = 6221
  video = 138

  if (len(sys.argv) > 1):
    totalFrame = min(int(sys.argv[1]), totalFrame)
    if (len(sys.argv) > 2):
      startFrame = min(int(sys.argv[2]), totalFrame)
    if (len(sys.argv) > 3):
      fm_num = int(sys.argv[3])
      if fm_num == 1:
        video = 134
      elif fm_num == 5:
        video = 138
      else:
        print('Error! please choose between 1 and 5')
        exit()
    if (len(sys.argv) > 4):
      outputBatchSize = min(outputBatchSize, int(sys.argv[4]))
      inputPrefix = 'protobin-fused-local/example3_{}_{}'.format(video, 
                                                        outputBatchSize)

  for startFrame in xrange(0, totalFrame, WORK_PACKET_SIZE):
    event = {
      'inputBucket': inputBucket,
      'inputPrefix': inputPrefix,
      'startFrame': startFrame,
      'outputBatchSize': outputBatchSize,
      'outputPrefix': outputPrefix
    }
    start = now()
    result = handler(event, {})
    end = now()
    duration = (end - start) * 1000
    billedDuration = math.ceil(duration / 100.0) * 100.0
    print('Duration: {:.2f} ms Billed Duration: {:.0f} ms   Memory Size: 1536 MB  Max Memory Used: 1536 MB'.format(duration, billedDuration))
