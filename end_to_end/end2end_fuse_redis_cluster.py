######################################################
# -*- coding: utf-8 -*-
# File Name: end2end_fuse.py
# Author: Qian Li
# Created Date: 2017-12-14
# Description: The entry for all fused models!
######################################################

from scannerpy import Database, Job, ColumnType, DeviceType, BulkJob
from scannerpy.stdlib import parsers
import sys
import os.path
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) # execution path!
sys.path.append('../tests')
import util
from timeit import default_timer as now
import time
import math
from urllib import urlretrieve
import boto3
import botocore
from multiprocessing.pool import ThreadPool
from threading import Semaphore, Lock
import progressbar
import json
from collections import OrderedDict
import argparse
from rediscluster import StrictRedisCluster

import logging
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

LAMBDA_NAME = "fused-decode-hist-redis"

DEFAULT_KEEP_OUTPUT = False
MAX_PARALLEL_UPLOADS = 20

DEFAULT_OUTPUT_DIR = './'
PROTO_EXT = 'proto'
BIN_EXT = 'bin'
OUT_EXT = 'out'

DECODER_PATH = '/tmp/FusedDecodeHist-static'

TIMEOUT_SECONDS = 300.0 # maximum wait time

timelist = OrderedDict()

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--video', '-v', type=int, required=False,
            dest='video',
            default=1,
            help='Which video, choose from 1~4')
  parser.add_argument('--resolution', '-r', type=int, required=False,
            dest='resolution',
            default=1,
            help='Which resolution, choose from 1~5 (360p - 4K)')
  parser.add_argument('--outdir', '-o', type=str, required=False,
            dest='outDir',
            default=DEFAULT_OUTPUT_DIR,
            help='Directory to save log files')
  parser.add_argument('--batch', '-b', type=int, required=True,
            dest='batch',
            help='Batch size')
  parser.add_argument('--function', '-f', type=str, required=True,
            dest='lambdaName',
            help='Which lambda function to use')
  parser.add_argument('--upload-bucket', '-ub', type=str, required=True,
            dest='uploadBucket',
            help='Intermediate files upload bucket')
  parser.add_argument('--upload-prefix', '-up', type=str, required=False,
            dest='uploadPrefix',
            default='fused-protobin',
            help='Intermediate files upload prefix')
  parser.add_argument('--download-bucket', '-db', type=str, required=True,
            dest='downloadBucket',
            help='Output files bucket')
  parser.add_argument('--download-prefix', '-dp', type=str, required=False,
            dest='downloadPrefix',
            default='fused-output',
            help='Output files prefix')
  parser.add_argument('--timeout', '-t', type=int, required=False,
            dest='timeout',
            default=TIMEOUT_SECONDS,
            help='Time out in seconds (default 300s)')
  parser.add_argument('--redishostaddr', '-ip', type=str, required=False,
            dest='redis_hostaddr',
            default=None,
            help='Redis hostname public IP address')

  return parser.parse_args()

def list_output_files(outputDir = DEFAULT_OUTPUT_DIR, fileExt = None):
  if fileExt == None:
    print('Please provide file extension: e.g., .jpg, .bin')
    exit()
  fileExt = '.{0}'.format(fileExt)
  outputFiles = [
    x for x in os.listdir(outputDir) if x.endswith(fileExt)
  ]
  return outputFiles

def ensure_clean_state(videoPath, batch, bucketName, prefix, args):
  print('Cleaning the local folder')
  for fileName in list_output_files(DEFAULT_OUTPUT_DIR, PROTO_EXT):
      localFilePath = os.path.join(DEFAULT_OUTPUT_DIR, fileName)
      print('Cleaning: {}'.format(localFilePath))
      os.remove(localFilePath)

  for fileName in list_output_files(DEFAULT_OUTPUT_DIR, BIN_EXT):
      localFilePath = os.path.join(DEFAULT_OUTPUT_DIR, fileName)
      print('Cleaning: {}'.format(localFilePath))
      os.remove(localFilePath)

  
  videoPrefix = videoPath.split(".")[-2].split("/")[-1]
  print('Cleaning Redis db: {}/{}/{}_{}_{}/'.format(bucketName, 
    prefix, videoPrefix, batch, batch))
  #rclient = StrictRedisCluster(startup_nodes=[{"host": args.redis_hostaddr, "port": "6379"}], decode_responses=False)
  rclient = StrictRedisCluster(startup_nodes=[{"host": "elasticache2-4xl.e4lofi.clustercfg.usw2.cache.amazonaws.com", "port": "6379"}], 
						decode_responses=False, skip_full_coverage_check=True)
  fileCount = 0
  for obj in rclient.keys('{}/{}_{}_{}/*'.format(prefix, videoPrefix, 
                                   batch, batch)):
    rclient.delete(obj)	
    fileCount += 1

  print('Deleted {} files'.format(fileCount))


# Upload all files with certain extension to a bucket
uploadFileCount = 0
def upload_output_to_redis(bucketName, filePrefix, fileExt, args):
  print('Uploading files to Redis: {:s}/{:s}'.format(bucketName, filePrefix))
  #rclient = redis.Redis(host=args.redis_hostaddr, port=6379, db=0)
  rclient = StrictRedisCluster(startup_nodes=[{"host": "elasticache2-4xl.e4lofi.clustercfg.usw2.cache.amazonaws.com", "port": "6379"}], 
						decode_responses=False, skip_full_coverage_check=True)
  s3 = boto3.client('s3', config=botocore.client.Config(
    max_pool_connections=MAX_PARALLEL_UPLOADS))
  
  urlretrieve("https://s3-us-west-2.amazonaws.com/mxnet-params/FusedDecodeHist-static", DECODER_PATH)
  f = open(DECODER_PATH, 'rb')
  data = f.read()
  f.close()
  rclient.set("FusedDecodeHist-static", data)
  
  global uploadFileCount
  uploadFileCount = 0
  countLock = Lock()
  totalSize = 0

  maxval = sum(1 for _ in list_output_files(DEFAULT_OUTPUT_DIR, fileExt))

  bar = progressbar.ProgressBar(maxval=maxval,
    widgets=[progressbar.Bar('=', 'Uploaded  [', ']'), ' ',
             progressbar.Percentage()])
  bar.start()

  def upload_file(localFilePath, uploadFileName, fileSize, rclient):

    try:
      with open(localFilePath, 'rb') as ifs:
        data = ifs.read()
	ifs.close()
	rclient.set(uploadFileName, data)
    finally:
      global uploadFileCount
      with countLock:
        uploadFileCount += 1
      bar.update(uploadFileCount)
      if DEFAULT_KEEP_OUTPUT == False:
          os.remove(localFilePath)

  for fileName in list_output_files(DEFAULT_OUTPUT_DIR, fileExt):
    localFilePath = os.path.join(DEFAULT_OUTPUT_DIR, fileName)
    uploadFileName = os.path.join(filePrefix, fileName)
    fileSize = os.path.getsize(localFilePath)

    # FIXME: why was parallel upload an issue?
    ifs = open(localFilePath, 'rb')
    data = ifs.read()
    ifs.close()
    rclient.set(uploadFileName, data)
    uploadFileCount += 1
 
    totalSize += fileSize
    
  bar.finish()

  print('Uploaded {:d} files to Redis [total={:d}KB]'.format(uploadFileCount, 
    totalSize >> 10))

  return (uploadFileCount, totalSize)

# Invoke lambdas and return the count
lambdaCount = 0
def invoke_lambdas(numFrames, args):
  batch = args.batch
  lambdaTotalCount = len(xrange(0, numFrames, batch))
  bar = progressbar.ProgressBar(maxval=lambdaTotalCount,
        widgets=[progressbar.Bar('=', 'Lambdas   [', ']'), ' ',
                 progressbar.Percentage()])
  bar.start()
  global lambdaCount
  lambdaCount = 0
  pool = ThreadPool(MAX_PARALLEL_UPLOADS)
  sema = Semaphore(MAX_PARALLEL_UPLOADS)
  countLock = Lock()
  results = []

  def invoke_lambda(startFrame, args):
    sema.acquire()
    successCount = 1
    try:
      client = boto3.client('lambda')
      payload = OrderedDict()
      payload['inputBucket'] = args.uploadBucket
      payload['inputPrefix'] = args.uploadPrefix
      payload['outputBatchSize'] = args.batch
      payload['startFrame'] = startFrame
      payload['outputBucket'] = args.downloadBucket
      payload['outputPrefix'] = args.downloadPrefix

      response = client.invoke(FunctionName=args.lambdaName,
                               InvocationType='Event',
                               Payload=str.encode(json.dumps(payload)))

      if response['StatusCode'] != 202:
        print('Error in invoking Lambda start from #{:d}'.format(startFrame))
        successCount = 0

    finally:
      sema.release()
      global lambdaCount
      with countLock:
        lambdaCount += successCount
      bar.update(lambdaCount)

  for startFrame in xrange(0, numFrames, batch):
    result = pool.apply_async(invoke_lambda, args=(startFrame, args))
    results.append(result)

  for result in results:
    result.get()

  for _ in xrange(MAX_PARALLEL_UPLOADS):
    sema.acquire()
  bar.finish()

  return lambdaCount


# Wait until all output files appear in Redis, return # files
def wait_until_all_finished(startFrame, numFrames, videoPrefix, args):
  batch = args.batch
  totalCount = len(xrange(startFrame, numFrames, batch))
  rclient = StrictRedisCluster(startup_nodes=[{"host": "elasticache2-4xl.e4lofi.clustercfg.usw2.cache.amazonaws.com", "port": "6379"}], 
						decode_responses=False, skip_full_coverage_check=True)
  outputBucket = args.downloadBucket
  outputPrefix = args.downloadPrefix

  bar = progressbar.ProgressBar(maxval=totalCount, \
    widgets=[progressbar.Bar('=', 'Files     [', ']'), ' ', 
             progressbar.Percentage()])
  bar.start()

  fileCount = 0
  time.sleep(2.0) # sleep for 2 seconds to wait for decoder finished!
  startTime = now()
  timeOut = startTime + args.timeout
  while fileCount < totalCount:
    # list the number of objects
    fileCount = len(rclient.keys('{}/{}_{}_{}/*'.format(outputPrefix, videoPrefix, batch, batch)))
    bar.update(fileCount)
    if fileCount >= totalCount:
      break

    currTime = now()
    if currTime >= timeOut:
      print('Timed out in {:.4f} sec, cannot finish.'.format(currTime - startTime))
      break
      
    time.sleep(0.1)
  bar.finish()
  return fileCount


def start_fuse_pipeline(videoPath, args):
  global timelist

  if util.have_gpu():
    device = DeviceType.GPU
    print('has GPU device!')
  else:
    device = DeviceType.CPU
    print('only has CPUs!')

  scriptDir = './'
  numFrames = 0

  batch = args.batch
  videoPrefix = videoPath.split(".")[-2].split("/")[-1]
  print('Video name is: {:s}'.format(videoPrefix))

  uploadPrefix = os.path.join(args.uploadPrefix, '{}_{}'.format(
                              videoPrefix, batch))
  args.uploadPrefix = uploadPrefix



  ###################################################
  # 0. Start Scanner DB
  # Use its load worker to generate .proto and .bin files
  ###################################################
  with Database() as db:
    # Register the fake kernel
    db.register_op('Fake', [('frame', ColumnType.Video)], ['class'])
    kernelPath = os.path.join(scriptDir, 'fake_op.py')
    db.register_python_kernel('Fake', device, kernelPath, batch = 10)

    ####################
    # Ingest the video
    ####################
    start = now()
    [input_table], failed = db.ingest_videos([ 
        ('end2end_fused_raw', videoPath)], force=True)
    stop = now()
    delta = stop - start
    print('Time to ingest videos: {:.4f}s, fps: {:.4f}'.format(
      delta, input_table.num_rows() / delta))
    timelist["ingest-video"] = delta

    numFrames = input_table.num_rows()
    print('Number of frames in movie: {:d}'.format(numFrames))

    if len(failed) > 0:
      print('Failures:', failed)

    ######################
    # Prepare decode data
    ######################
    start = now()
    frame = db.ops.FrameInput()
    classes = db.ops.Fake(frame = frame, batch = batch)
    output_op = db.ops.Output(columns=[classes])
    job = Job(
      op_args={
        frame: input_table.column('frame'),
        output_op: 'end2end_fused_out'
      }
    )
    bulk_job = BulkJob(output=output_op, jobs=[job])
    [output_table] = db.run(bulk_job, force=True, profiling=False, pipeline_instances_per_node=1, load_to_disk=True, 
      work_packet_size=batch)

    stop = now()
    delta = stop - start
    print('Batch: {:d} Decode preparation time: {:.4f}s, {:.1f} fps\n'.format(batch, delta, numFrames / delta))
    timelist["pre-decode"] = delta

  ###################################################
  # 1. Start the Lambda part
  # Use Lambdas to decode and evaluate kernels
  ###################################################

  ######################
  # 1.0 Upload all .proto files
  ######################
  uploadBucket = args.uploadBucket
  start = now()
  fileCount, totalSize = upload_output_to_redis(
    uploadBucket, uploadPrefix, PROTO_EXT, args)

  ######################
  # 1.1 Upload all .bin files
  ######################
  fileCount, totalSize = upload_output_to_redis(
    uploadBucket, uploadPrefix, BIN_EXT, args)
  stop = now()
  delta = stop - start
  print('Upload args to Redis time: {:.4f} s'.format(delta))
  timelist["upload-redis"] = delta

  ################################################
  # 1.2 Call Lambdas to decode + evaluate, 
  # provide Bucket Name, File Prefix, numFrames, batch
  ################################################
  start = now()
  lambdaCount = invoke_lambdas(numFrames, args)
  stop = now()
  delta = stop - start
  print('Triggered #{} Lambdas, time {:.4f} s'.format(lambdaCount, delta))
  timelist["invoke-lambda"] = delta

  ################################################
  # 1.3 Wait until all output files appear
  ################################################
  fileCount = wait_until_all_finished(0, numFrames, videoPrefix, args)
  totalCount = len(xrange(0, numFrames, batch)) 
  print('Collected {:d} out of {:d} files, error rate: {:.4f}'.format(
    fileCount, totalCount, (totalCount - fileCount) * 1.0 / totalCount))

def main(args):
  print('Argument list: {}'.format(args))

  videoNum = args.video # video num
  videoRes = args.resolution # resolution
  outDir = args.outDir # logs directory
  batch = args.batch
  outputBucket = args.downloadBucket
  outputPrefix = args.downloadPrefix

  ###################################################
  # 0. Download the video
  ###################################################
  videoPath = util.download_video1(videoNum, videoRes)

  ###################################################
  # 1. Clean previous output files
  ###################################################
  ensure_clean_state(videoPath, batch, outputBucket, outputPrefix, args)

  ###################################################
  # 2. The main fuse pipeline
  ###################################################
  start = now()
  start_fuse_pipeline(videoPath, args)
  stop = now()
  delta = stop - start
  print('Total pipeline time is: {:.4f} s'.format(delta))
  timelist["total-time"] = delta

  ###################################################
  # 3. Prepare output logs
  ###################################################
  outString = "Timelist:" + json.dumps(timelist)
  print(outString)

  outFile =  os.path.join(outDir, 'end2end_fuse_{}_{}_{}.out'.format(
    videoNum, videoRes, batch))
  with open(outFile, 'w') as ofs:
    ofs.write(outString)
  print('Save log to {}'.format(outFile))

if __name__ == '__main__':
  main(get_args())
