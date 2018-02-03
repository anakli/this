## Simple lambda microbenchmark for unloaded latency tests

import time
import sys
import redis


REQ_SIZE = 1024 # use 1KB for unloaded latency tests 
NUM_TRIALS = 1000
REDIS_HOSTADDR_PRIV = "elasti8xl.e4lofi.0001.usw2.cache.amazonaws.com" #TODO: set to correct url


def put_key(rclient, key, data):
    
  start_time = time.time()
  rclient.set(key, data) 
  end_time = time.time()
    
  elapsed_time = (end_time - start_time) * 1000 * 1000
  #print "Elapsed SET: %d us" % elapsed_time
  return elapsed_time

def get_key(rclient, key):
    
  start_time = time.time()
  rclient.get(key) 
  end_time = time.time()
    
  elapsed_time = (end_time - start_time) * 1000 * 1000
  #print "Elapsed GET: %d us" % elapsed_time
  return elapsed_time

def main():
  put_times = []
  get_times = []
  rclient = redis.Redis(host=REDIS_HOSTADDR_PRIV, port=6379, db=0)  
  data = open("/dev/urandom","rb").read(REQ_SIZE)
  for i in xrange(NUM_TRIALS):
    elapsed_time = put_key(rclient, "key" + str(i), data)
    if i > 2:
      put_times.append(elapsed_time)
  for i in xrange(NUM_TRIALS):
    elapsed_time = get_key(rclient, "key" + str(i))
    if i > 2:
      get_times.append(elapsed_time)
   
  avg_put_time = sum(put_times) / float(len(put_times))
  #p10_put_time = np.percentile(put_times, 10)
  #p90_put_time = np.percentile(put_times, 90)
  
  avg_get_time = sum(get_times) / float(len(get_times))
  #p10_get_time = np.percentile(get_times, 10)
  #p90_get_time = np.percentile(get_times, 90)

  print("PUT 1KB: avg=%dus \n GET 1KB: avg=%dus" % (
        avg_put_time, avg_get_time))

  #print "PUT:", put_times
  #print "GET:", get_times
  return {
    "message": 
      "PUT 1KB: avg=%dus \n GET 1KB: avg=%dus" % (
        avg_put_time, avg_get_time)
    }

if __name__ == "__main__":
  main()
