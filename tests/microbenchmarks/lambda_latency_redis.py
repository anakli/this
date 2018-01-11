## Simple lambda microbenchmark for unloaded latency tests

import time
import sys
import redis


REQ_SIZE = 1024 # use 1KB for unloaded latency tests 
NUM_TRIALS = 100
REDIS_HOSTADDR_PRIV = "elasti8xl.e4lofi.0001.usw2.cache.amazonaws.com" #TODO: set to correct url



def put_key(key):
  data = open("/dev/urandom","rb").read(REQ_SIZE)
  rclient = redis.Redis(host=REDIS_HOSTADDR_PRIV, port=6379, db=0)  
    
  start_time = time.time()
  rclient.set(key, data) 
  end_time = time.time()
    
  elapsed_time = (end_time - start_time) * 1000 * 1000
  #print "Elapsed SET: %d us" % elapsed_time
  return elapsed_time

def get_key(key):
  rclient = redis.Redis(host=REDIS_HOSTADDR_PRIV, port=6379, db=0)  
    
  start_time = time.time()
  rclient.get(key) 
  end_time = time.time()
    
  elapsed_time = (end_time - start_time) * 1000 * 1000
  #print "Elapsed GET: %d us" % elapsed_time
  return elapsed_time

def handler(event, context):
  put_times = []
  get_times = []
  for i in xrange(NUM_TRIALS):
    elapsed_time = put_key("key" + str(i))
    put_times.append(elapsed_time)
  for i in xrange(NUM_TRIALS):
    elapsed_time = get_key("key" + str(i))
    get_times.append(elapsed_time)
   
  avg_put_time = sum(put_times) / float(len(put_times))
  #p10_put_time = np.percentile(put_times, 10)
  #p90_put_time = np.percentile(put_times, 90)
  
  avg_get_time = sum(get_times) / float(len(get_times))
  #p10_get_time = np.percentile(get_times, 10)
  #p90_get_time = np.percentile(get_times, 90)

  print("PUT 1KB: avg=%dus \n GET 1KB: avg=%dus" % (
        avg_put_time, avg_get_time))

  print "PUT:", put_times
  print "GET:", get_times
  return {
    "message": 
      "PUT 1KB: avg=%dus \n GET 1KB: avg=%dus" % (
        avg_put_time, avg_get_time)
      #"PUT 1KB: avg=%dus, p10=%fus, p90=%fus \n GET 1KB: avg=%dus, p10=%fus, p90=%fus" % (
      #  avg_put_time, p10_put_time, p90_put_time, avg_get_time, p10_get_time, p90_get_time)
    }
