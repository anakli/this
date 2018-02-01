## Simple lambda microbenchmark for unloaded latency tests

import time
import sys
import ifcfg
import threading
import time
from threading import Timer
import shutil
import subprocess
import boto3
import botocore
from multiprocessing.pool import ThreadPool
from threading import Semaphore
import urllib2
from urllib import urlretrieve
from timeit import default_timer as now
import json
from collections import OrderedDict
import math
import os.path

REQ_SIZE = 1048576 # use 1MB for throughput tests
NUM_TRIALS = 1000
REDIS_HOSTADDR_PRIV = "elasti8xl.e4lofi.0001.usw2.cache.amazonaws.com" #TODO: set to correct url
LOGS_PATH="microbench-logs"
BUCKET="microbench-tests"

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

def upload_net_bytes(rxbytes_per_s, txbytes_per_s, timelogger, reqid):
  netstats = LOGS_PATH + '/netstats-' + reqid 
  s3 = boto3.client('s3')
  try:
    s3.put_object(Bucket=BUCKET, Key=netstats, Body=str({'lambda': reqid,
             'started': timelogger.start,
             'rx': rxbytes_per_s,
             'tx': txbytes_per_s,
             'ended': time.time()}).encode('utf-8'))
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
      print("The object does not exist.")
    else:
      raise
  print "wrote netstats"
  return

def upload_avg_bytes(rxbytes_per_s, txbytes_per_s, timelogger, reqid):
  #rclient = redis.Redis(host=REDIS_HOSTADDR_PRIV, port=6379, db=0)  
  netstats = LOGS_PATH + '/netstats-' + reqid 
  s3 = boto3.client('s3')
  try:
    s3.put_object(Bucket=BUCKET, Key=netstats, Body=str({'lambda': reqid,
             'started': timelogger.start,
             'rx': rxbytes_per_s,
             'tx': txbytes_per_s,
             'ended': time.time()}).encode('utf-8'))
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
      print("The object does not exist.")
    else:
      raise
  return
  
def upload_s3(s3, bucketName, localFilePath, uploadFileName, req_size, data):
  try:
    s3.put_object(Body=data, Bucket=bucketName, Key=uploadFileName)
  except botocore.exceptions.ClientError as e:
    print e
    raise

def download_s3(s3, bucketName, s3Path, localPath):
  try:
    s3.Bucket(bucketName).download_file(s3Path, localPath)
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
      print("The object does not exist.")
    else:
      raise

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


def put_key(s3, key, req_size, data):
    
  upload_s3(s3, BUCKET, "/tmp/" + key, key, req_size, data) 
  
  return 

def get_key(s3, key):
    
  #download_s3(s3, BUCKET, key, "/tmp/" + key) 
  #os.remove("/tmp/" + key)
  get_s3(s3, BUCKET, key) 
   
  return 

def handler(event, context):
  timelogger = TimeLog(enabled=True)
  num_trials = NUM_TRIALS
  req_size = REQ_SIZE
  if 'req_size' in event:
    req_size = event['req_size']
  else:
    print('Warning: using default req_size: ', REQ_SIZE)
  if 'num_trials' in event:
    num_trials = event['num_trials']
  else:
    print('Warning: using default num_trials: ', NUM_TRIALS)
  iface = ifcfg.default_interface()
  rxbytes = [int(iface['rxbytes'])]
  txbytes = [int(iface['txbytes'])]
  rxbytes_per_s = []
  txbytes_per_s = []
  #get_net_bytes(rxbytes, txbytes, rxbytes_per_s, txbytes_per_s)  
  
  put_times = []
  get_times = []

  txbytes_init = int(ifcfg.default_interface()['txbytes'])
  start_time = time.time()
  data = open("/dev/urandom","rb").read(req_size)
  s3 = boto3.client('s3')
  for i in xrange(num_trials):
    put_key(s3, "key" + str(context.aws_request_id) + str(i), req_size, data)
  end_time = time.time()
  txbytes_delta = int(ifcfg.default_interface()['txbytes']) - txbytes_init
  txbytes_throughput = (txbytes_delta * 8 / (end_time - start_time)) / 1e9
  put_throughput = ((num_trials * req_size * 8) / (end_time - start_time)) / 1e9
  
  rxbytes_init = int(ifcfg.default_interface()['rxbytes'])
  #s3 = boto3.resource('s3')
  start_time = time.time()
  for i in xrange(num_trials):
    get_key(s3, "key" + str(context.aws_request_id) + str(i))
   
  end_time = time.time()
  get_throughput = ((num_trials * req_size * 8) / (end_time - start_time)) / 1e9
  
  #upload_net_bytes(rxbytes_per_s, txbytes_per_s, timelogger, context.aws_request_id)
  upload_avg_bytes(get_throughput, put_throughput, timelogger, context.aws_request_id)
  rxbytes_delta = int(ifcfg.default_interface()['rxbytes']) - rxbytes_init
  rxbytes_throughput = (rxbytes_delta * 8 / (end_time - start_time)) / 1e9
  print "PUT (TX): ", put_throughput, " Gb/s ... ", txbytes_throughput 
  print "GET (RX): ", get_throughput, " Gb/s ... ", rxbytes_throughput

  return 


def main(args):
  print('Argument list: {}'.format(args))
  count = invoke_lambdas()
