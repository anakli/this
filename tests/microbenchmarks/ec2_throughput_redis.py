## Simple lambda microbenchmark for throughput tests

import time
import sys
import redis
import os.path

REQ_SIZE = (1048576) # use 1MB for throughput tests
NUM_TRIALS = 10000
REDIS_HOSTADDR_PRIV = "elasti8xl.e4lofi.0001.usw2.cache.amazonaws.com" #TODO: set to correct url
LOGS_PATH="microbench-logs"

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
    
def put_key(rclient, key, data):
    
  rclient.set(key, data) 
    
  return 

def get_key(rclient, key):
    
  rclient.get(key) 
    
  return 

def handler(req_size):
  timelogger = TimeLog(enabled=True)
  num_trials = NUM_TRIALS
  
  put_times = []
  get_times = []
  rclient = redis.Redis(host=REDIS_HOSTADDR_PRIV, port=6379, db=0)  

  data = open("/dev/urandom","rb").read(req_size)
  start_time = time.time()
  for i in xrange(num_trials):
    put_key(rclient, "key" + str(i), data)
  end_time = time.time()
  put_throughput = ((num_trials * req_size * 8) / (end_time - start_time)) / 1e9
  
  start_time = time.time()
  for i in xrange(num_trials):
    get_key(rclient, "key" + str(i))
  end_time = time.time()
  get_throughput = ((num_trials * req_size * 8) / (end_time - start_time)) / 1e9
  
  print "PUT (TX): ", put_throughput, " Gb/s ... " #, txbytes_throughput 
  print "GET (RX): ", get_throughput, " Gb/s ... " #, rxbytes_throughput

  return 


def main():
  for req_size in [1024, 1024*8, 1024*128, 1024 * 1024, 1024*1024*8, 1024*1024*128]:
    print "req_size: ", req_size
    handler(req_size)

if __name__ == "__main__":
  main()

