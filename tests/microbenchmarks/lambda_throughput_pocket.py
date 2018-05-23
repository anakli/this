## Simple lambda microbenchmark for throughput tests

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
import pocket

REQ_SIZE = (1048576) # use 1MB for throughput tests
NUM_TRIALS = 1000
#REDIS_HOSTADDR_PRIV = "elasti8xl.e4lofi.0001.usw2.cache.amazonaws.com" #TODO: set to correct url
LOGS_PATH="microbench-logs"
NAMENODE_IP = '10.1.0.10'
NAMENODE_PORT = 9070

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

def upload_net_bytes(rclient, rxbytes_per_s, txbytes_per_s, timelogger, reqid):
  #rclient = redis.Redis(host=REDIS_HOSTADDR_PRIV, port=6379, db=0)  
  netstats = LOGS_PATH + '/netstats-' + reqid 
  rclient.set(netstats, str({'lambda': reqid,
             'started': timelogger.start,
             'rx': rxbytes_per_s,
             'tx': txbytes_per_s,
             'ended': time.time()}).encode('utf-8'))
  print "wrote netstats"
  return

def upload_avg_bytes(p, rxbytes_per_s, txbytes_per_s, timelogger, reqid):
  netstats = LOGS_PATH + '/netstats-' + reqid 
  # FIXME: update this to write to file first then can write to pocket
  p.put(p, netstats, str({'lambda': reqid,
             'started': timelogger.start,
             'rx': rxbytes_per_s,
             'tx': txbytes_per_s,
             'ended': time.time()}).encode('utf-8'))
  return
  
def put_key(p, key, filename): 
  pocket.put(p, filename, key, '')  
  #rclient.set(key, data) 
    
  return 

def get_key(p, key):
  pocket.get(p, key, '/tmp/get-dst', '')  
  #rclient.get(key) 
    
  return 

def handler(event, context):
  timelogger = TimeLog(enabled=True)
  num_trials = NUM_TRIALS
  req_size = REQ_SIZE
  p = pocket.connect(NAMENODE_IP, NAMENODE_PORT)
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
  
  put_times = []
  get_times = []
  #rclient = redis.Redis(host=REDIS_HOSTADDR_PRIV, port=6379, db=0)  

  txbytes_init = int(ifcfg.default_interface()['txbytes'])
  #data = open("/dev/urandom","rb").read(req_size)
  filename = '/tmp/data_file'
  with open(filename, 'wb') as fout:
    fout.write(os.urandom(req_size))
  start_time = time.time()
  for i in xrange(num_trials):
    put_key(p, "key" + str(context.aws_request_id) + str(i), filename)
  end_time = time.time()
  txbytes_delta = int(ifcfg.default_interface()['txbytes']) - txbytes_init
  txbytes_throughput = (txbytes_delta * 8 / (end_time - start_time)) / 1e9
  put_throughput = ((num_trials * req_size * 8) / (end_time - start_time)) / 1e9
  
  rxbytes_init = int(ifcfg.default_interface()['rxbytes'])
  start_time = time.time()
  for i in xrange(num_trials):
    get_key(p, "key" + str(context.aws_request_id) + str(i))
  end_time = time.time()
  get_throughput = ((num_trials * req_size * 8) / (end_time - start_time)) / 1e9
  
  #upload_net_bytes(rclient, rxbytes_per_s, txbytes_per_s, timelogger, context.aws_request_id)
  #upload_avg_bytes(p, get_throughput, put_throughput, timelogger, context.aws_request_id)
  rxbytes_delta = int(ifcfg.default_interface()['rxbytes']) - rxbytes_init
  rxbytes_throughput = (rxbytes_delta * 8 / (end_time - start_time)) / 1e9
  print "PUT (TX): ", put_throughput, " Gb/s ... ", txbytes_throughput 
  print "GET (RX): ", get_throughput, " Gb/s ... ", rxbytes_throughput

  return 


def main(args):
  print('Argument list: {}'.format(args))
  count = invoke_lambdas()
