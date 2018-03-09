import os
import sys
import shutil
import subprocess
import boto3
import botocore
import hashlib
import struct 
from multiprocessing.pool import ThreadPool
from threading import Semaphore
import urllib2
from urllib import urlretrieve
from timeit import default_timer as now
import json
from collections import OrderedDict
import math
import time
import ifcfg
import threading
import psutil

DECODER_PATH = '/tmp/DecoderAutomataCmd-static'
TEMP_OUTPUT_DIR = '/tmp/output'
LOCAL_INPUT_DIR = '/tmp/input'
WORK_PACKET_SIZE = 50

INPUT_BUCKET = 'video-lambda-input'
OUTPUT_BUCKET = 'video-lambda-input-results'

# os.environ['LD_LIBRARY_PATH'] = '$%s:%s/scanner/' % (os.environ['LD_LIBRARY_PATH'], os.getcwd())
DEFAULT_LOG_LEVEL = 'warning'

DEFAULT_OUTPUT_BATCH_SIZE = 1
DEFAULT_KEEP_OUTPUT = False

MAX_PARALLEL_UPLOADS = 20

OUTPUT_FILE_EXT = 'jpg'

LOGS_BUCKET= 'video-lambda-logs'

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
    

def get_net_bytes(rxbytes, txbytes, rxbytes_per_s, txbytes_per_s, cpu_util):
  SAMPLE_INTERVAL = 1.0
  threading.Timer(SAMPLE_INTERVAL, get_net_bytes, [rxbytes, txbytes, rxbytes_per_s, txbytes_per_s]).start() # schedule the function to execute every SAMPLE_INTERVAL seconds
  rxbytes.append(int(ifcfg.default_interface()['rxbytes']))
  txbytes.append(int(ifcfg.default_interface()['txbytes']))
  rxbytes_per_s.append((rxbytes[-1] - rxbytes[-2])/SAMPLE_INTERVAL)
  txbytes_per_s.append((txbytes[-1] - txbytes[-2])/SAMPLE_INTERVAL)
  util = psutil.cpu_percent(interval=1)
  cpu_util.append(util)

def upload_timelog(timelogger, reqid):
  s3 = boto3.client('s3')
  s3.put_object(
    ACL='public-read',
    Bucket=LOGS_BUCKET,
    Key=reqid,
    Body=str({'lambda': reqid,
             'started': timelogger.start,
             'timelog': timelogger.points}).encode('utf-8'),
    StorageClass='REDUCED_REDUNDANCY')
  print "wrote timelog"
  return

def upload_net_bytes(rxbytes_per_s, txbytes_per_s, cpu_util, timelogger, reqid):
  s3 = boto3.client('s3')
  s3.put_object(
    ACL='public-read',
    Bucket=LOGS_BUCKET+"-netstats",
    Key=reqid,
    Body=str({'lambda': reqid,
             'started': timelogger.start,
             'rx': rxbytes_per_s,
             'tx': txbytes_per_s,
             'cpu': cpu_util}).encode('utf-8'),
    StorageClass='REDUCED_REDUNDANCY')
  print "wrote netstats"
  return

def list_output_files():
  fileExt = '.{0}'.format(OUTPUT_FILE_EXT)
  outputFiles = [
    x for x in os.listdir(TEMP_OUTPUT_DIR) if x.endswith(fileExt)
  ]
  return outputFiles

def many_files_to_one(inPaths, outPath):
  with open(outPath, 'wb') as ofs:
    for filePath in inPaths:
      with open(filePath, 'rb') as ifs:
        data = ifs.read()
        dataLen = len(data)
        fileName = os.path.basename(filePath)
        ofs.write(struct.pack('I', len(fileName)))
        ofs.write(fileName)
        ofs.write(struct.pack('I', dataLen))
        ofs.write(data)
      os.remove(filePath) # delete here!
  print 'Wrote', outPath

def combine_output_files(startFrame, outputBatchSize):
  def encode_batch(batch):
    inputFilePaths = [
      os.path.join(TEMP_OUTPUT_DIR, x) for x in batch
    ]
    name, ext = os.path.splitext(batch[0])
    outputFilePath = os.path.join(
      TEMP_OUTPUT_DIR, '%s-%d%s' % (name, len(batch), ext))
    print "encode batch file: " + outputFilePath
    many_files_to_one(inputFilePaths, outputFilePath)
    # for filePath in inputFilePaths:
    #   os.remove(filePath)

  # Guarantee the sequence and order! otherwise, "20" > "100" because of
  # the character order
  currentBatch = []
  outputFiles = list_output_files()
  totalNum = len(outputFiles)
  remain = totalNum
  for currStart in xrange(startFrame, startFrame + totalNum, outputBatchSize):
    currEnd = min(remain, outputBatchSize) + currStart
    for idx in xrange(currStart, currEnd):
      fileName = 'frame{:d}.jpg'.format(idx)
      if fileName not in outputFiles:
        print('ERROR: Cannot find file: {:s}'.format(fileName))
        exit()
      currentBatch.append(fileName)
    encode_batch(currentBatch)
    currentBatch = []
    remain -= outputBatchSize
  return totalNum

def download_input_from_s3(bucketName, inputPrefix, startFrame):
  def download_s3(s3Path, localPath):
    try:
      s3.Bucket(bucketName).download_file(s3Path, localPath)
    except botocore.exceptions.ClientError as e:
      if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
      else:
        raise

  protoFileName = 'decode_args{:d}.proto'.format(startFrame)
  binFileName = 'start_frame{:d}.bin'.format(startFrame)
  print('Downloading files {:s} and {:s} for batch {:d} \
        from s3: {:s}/{:s}'.format(protoFileName, binFileName, startFrame, 
          bucketName, inputPrefix))
  s3 = boto3.resource('s3')
  s3ProtoName = inputPrefix + '/' + protoFileName
  s3BinName = inputPrefix + '/' + binFileName
  protoPath = LOCAL_INPUT_DIR + '/' + protoFileName
  binPath = LOCAL_INPUT_DIR + '/' + binFileName
  
  download_s3(s3ProtoName, protoPath)
  download_s3(s3BinName, binPath)

  return protoPath, binPath

def upload_output_to_s3(bucketName, filePrefix):
  print('Uploading files to s3: {:s}/{:s}'.format(bucketName, filePrefix))
  s3 = boto3.client('s3', config=botocore.client.Config(
    max_pool_connections=MAX_PARALLEL_UPLOADS))

  count = 0
  totalSize = 0
  results = []

  pool = ThreadPool(MAX_PARALLEL_UPLOADS)
  sema = Semaphore(MAX_PARALLEL_UPLOADS)

  def upload_file(localFilePath, uploadFileName, fileSize):
    sema.acquire()
    try:
      print 'Start: %s [%dKB]' % (localFilePath, fileSize >> 10)
      with open(localFilePath, 'rb') as ifs:
        s3.put_object(Body=ifs, Bucket=bucketName,
          Key=uploadFileName,
          StorageClass='REDUCED_REDUNDANCY')
      print 'Done: %s' % localFilePath
    finally:
      sema.release()

  for fileName in list_output_files():
    localFilePath = os.path.join(TEMP_OUTPUT_DIR, fileName)
    uploadFileName = os.path.join(filePrefix, fileName)
    fileSize = os.path.getsize(localFilePath)

    result = pool.apply_async(upload_file, 
      args=(localFilePath, uploadFileName, fileSize))
    results.append(result)

    count += 1
    totalSize += fileSize

  # block until all threads are done
  for result in results:
    result.get()

  # block until all uploads are finished
  for _ in xrange(MAX_PARALLEL_UPLOADS):
    sema.acquire()

  print 'Uploaded %d files to S3 [total=%dKB]' % (count, totalSize >> 10)
  return (count, totalSize)

def list_output_directory():
  print '%s/' % TEMP_OUTPUT_DIR
  count = 0
  totalSize = 0
  for fileName in list_output_files():
    localFilePath = os.path.join(TEMP_OUTPUT_DIR, fileName)
    fileSize = os.path.getsize(localFilePath)
    print ' [%04dKB] %s' % (fileSize >> 10, fileName)
    totalSize += fileSize
    count += 1
  print 'Generated %d files [total=%dKB]' % (count, totalSize >> 10)
  return (count, totalSize)

def ensure_clean_state():
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
  #shutil.copy('DecoderAutomataCmd-static', DECODER_PATH)
  print "downloading decoder..."
  s3 = boto3.resource('s3')
  s3.Bucket('anakli').download_file('DecoderAutomataCmd-static', DECODER_PATH)
  #urlretrieve("https://s3-us-west-2.amazonaws.com/anakli/DecoderAutomataCmd-static", DECODER_PATH)
  os.chmod(DECODER_PATH, 0o755)
  print "downloaded decoder."
  subprocess.call(["ls", "-al", "/tmp"])

def convert_to_jpegs(protoPath, binPath):
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
  print protoPath, binPath
  return rc == 0


def invoke_mxnet_lambdas(bucketName, filePrefix):
  client = boto3.client('lambda')
  for fileName in list_output_files():
    localFilePath = os.path.join(TEMP_OUTPUT_DIR, fileName)
    uploadFileName = os.path.join(filePrefix, fileName)

    payload = '{{ \"b64Img\": \"{:s}\"}}'.format(uploadFileName) #FIXME: is listing output_files going to work like this?
    # TODO: no, the image upload to S3 is already bundled, just upload the result as one item, mxnet lambda will parse it by itself
    response = client.invoke(FunctionName='mxnet-lambda',
                           InvocationType='Event',
                           Payload=str.encode(payload))

    if response['StatusCode'] == 202:
      print("Invoke mxnet lambda" + uploadFileName)
    else:
      print("Failed to invoke mxnet lambda" + uploadFileName)
      return False
  return True


def handler(event, context):
  timelist = OrderedDict()
  timelogger = TimeLog(enabled=True)
  iface = ifcfg.default_interface()
  rxbytes = [int(iface['rxbytes'])]
  txbytes = [int(iface['txbytes'])]
  rxbytes_per_s = []
  txbytes_per_s = []
  cpu_util = []
  get_net_bytes(rxbytes, txbytes, rxbytes_per_s, txbytes_per_s, cpu_util)  

  start = now()
  ensure_clean_state()
  end = now()
  timelogger.add_point("prepare decoder")
  print('Time to prepare decoder: {:.4f} s'.format(end - start))
  # timelist += '"prepare-decoder" : %f,' % (end - start)
  timelist["prepare-decoder"] = (end - start)

  inputBucket = INPUT_BUCKET #'vass-video-samples2'
  inputPrefix = 'protobin/example3_134'
  startFrame = 0
  outputBatchSize = 1

  outputBucket = OUTPUT_BUCKET #"vass-video-samples2-results"
  outputPrefix = "decode-output"
  
  if 'inputBucket' in event:
    inputBucket = event['inputBucket']
    # outputBucket = inputBucket + '-results'
    outputBucket = inputBucket
  else:
    print('Warning: using default input bucket: {:s}'.format(inputBucket))
  if 'inputPrefix' in event:
    inputPrefix = event['inputPrefix']
    # get the video name!
    # outputPrefix = outputPrefix + '/' + inputPrefix.split('/')[-1] 
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
  protoPath, binPath = download_input_from_s3(inputBucket, inputPrefix, 
                                              startFrame)
  end = now()
  timelogger.add_point("download_inputs")
  print('Time to download input files: {:.4f} s'.format(end - start))
  # timelist += '"download-input" : %f,' % (end - start)
  timelist["download-input"] = (end - start)

  inputBatch = 0
  try:
    try:
      start = now()
      if not convert_to_jpegs(protoPath, binPath):
        raise Exception('Failed to decode video chunk {:d}'.format(startFrame))
      end = now()
      print('Time to decode: {:.4f} '.format(end - start))
      # timelist += '"decode" : %f,' % (end - start)
      timelist["decode"] = (end - start)
    finally:
      shutil.rmtree(LOCAL_INPUT_DIR)

    start = now()
    if outputBatchSize > 1:
      inputBatch = combine_output_files(startFrame, outputBatchSize)
    end = now()
    print('Time to combine output files: {:.4f} '.format(end - start))
    # timelist += '"combine-output" : %f,' % (end - start)
    timelist["combine-output"] = (end - start)
    timelogger.add_point("decode and combine output")

    start = now()
    fileCount, totalSize = upload_output_to_s3(outputBucket, outputPrefix)
    end = now()
    if outputBatchSize == 1:
      inputBatch = fileCount
    print('Time to upload output files: {:.4f} '.format(end - start))
    # timelist += '"upload-output" : %f,' % (end - start)
    timelist["upload-output"] = (end - start)
    timelogger.add_point("upload output")
  finally:
    invoke_mxnet_lambdas(outputBucket, outputPrefix)
    start = now()
    if not DEFAULT_KEEP_OUTPUT:
      shutil.rmtree(TEMP_OUTPUT_DIR)
    end = now()
    print('Time to clean output files: {:.4f} '.format(end - start))
    # timelist += '"clean-output" : %f,' % (end - start)
    timelist["clean-output"] = (end - start)
  
  # timelist += '"input-batch" : %d' % (inputBatch)
  timelist["input-batch"] = inputBatch
  # timelist += '}'

  upload_timelog(timelogger, context.aws_request_id) 
  upload_net_bytes(rxbytes_per_s, txbytes_per_s, cpu_util, timelogger, context.aws_request_id)

  print 'Timelist:' + json.dumps(timelist)
  out = {
    'statusCode': 200,
    'body': {
      'fileCount': fileCount,
      'totalSize': totalSize
    }
  }
  return out


if __name__ == '__main__':
  inputBucket = INPUT_BUCKET #'vass-video-samples2'
  inputPrefix = 'protobin/example3_134_50'
  startFrame = 0
  outputBatchSize = 50
  outputPrefix = 'decode-local-test'
  totalFrame = 6221

  if (len(sys.argv) > 1):
    totalFrame = min(int(sys.argv[1]), totalFrame)

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
