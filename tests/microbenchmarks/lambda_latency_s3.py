## Simple lambda microbenchmark for unloaded latency tests

import time
import sys
import boto3
import botocore


REQ_SIZE = 1024 # use 1KB for unloaded latency tests 
NUM_TRIALS = 100

BUCKET="microbench-tests"

def upload_s3(s3, bucketName, localFilePath, uploadFileName, req_size):
  data = open("/dev/urandom","rb").read(req_size)
  try:
    s3.put_object(Body=data, Bucket=bucketName, Key=uploadFileName)
  except botocore.exceptions.ClientError as e:
    print e
    raise

def put_key(s3, key):
  #data = open("/dev/urandom","rb").read(REQ_SIZE)
  #open("/tmp/" + key, "wb").write(data) 

  start_time = time.time()
  upload_s3(s3, BUCKET, "/tmp/" + key, key, REQ_SIZE) 
  end_time = time.time()
    
  elapsed_time = (end_time - start_time) * 1000
  #print "Elapsed SET: %d ms" % elapsed_time
  return elapsed_time

def get_s3(s3, bucketName, s3Path):
  obj = s3.get_object(Bucket=bucketName, Key=s3Path)

  fileobj = obj['Body']
  blocksize = 1024*1024
  bytes_read = 0
  buf = fileobj.read(blocksize)
  while len(buf) > 0:
    bytes_read += len(buf)
    #m.update(buf)
    buf = fileobj.read(blocksize)


def download_s3(s3, bucketName, s3Path, localPath):
  try:
    s3.Bucket(bucketName).download_file(s3Path, localPath)
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
      print("The object does not exist.")
    else:
      raise

def get_key(s3, key):
  start_time = time.time()
  #download_s3(s3, BUCKET, key, "/tmp/" + key) 
  get_s3(s3, BUCKET, key)
  end_time = time.time()
    
  elapsed_time = (end_time - start_time) * 1000
  #print "Elapsed GET: %d ms" % elapsed_time
  return elapsed_time

def handler(event, context):
  put_times = []
  get_times = []
  s3 = boto3.client('s3')
  for i in xrange(NUM_TRIALS):
    elapsed_time = put_key(s3, "key" + str(i))
    put_times.append(elapsed_time)
  for i in xrange(NUM_TRIALS):
    elapsed_time = get_key(s3, "key" + str(i))
    get_times.append(elapsed_time)
   
  avg_put_time = sum(put_times) / float(len(put_times))
  #p10_put_time = np.percentile(put_times, 10)
  #p90_put_time = np.percentile(put_times, 90)
  
  avg_get_time = sum(get_times) / float(len(get_times))
  #p10_get_time = np.percentile(get_times, 10)
  #p90_get_time = np.percentile(get_times, 90)

  print("PUT 1KB: avg=%dms \n GET 1KB: avg=%dms" % (
        avg_put_time, avg_get_time))
  
  print "PUT:", put_times
  print "GET:", get_times
  return {
    "message": 
      "PUT 1KB: avg=%dus \n GET 1KB: avg=%dus" % (
        avg_put_time, avg_get_time)
    }
