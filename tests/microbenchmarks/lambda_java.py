## Simple lambda microbenchmark for unloaded latency tests

import time
import sys
import os
import crail
from subprocess import call, Popen

def handler(event, context):
  crail.launch_dispatcher()
  
  call(["cp", "/var/task/conf/crail-site.conf", "/tmp/crail-site.conf"]) 
  call(["cp", "/var/task/conf/log4j.properties", "/tmp/log4j.properties"]) 
  call(["cp", "/var/task/conf/slaves", "/tmp/slaves"]) 
  call(["cp", "/var/task/conf/test.data", "/tmp/test"]) 
  call(["cp", "/var/task/lambda_java.py", "/tmp/lambda"]) 
  call(["cp", "/var/task/jars/crail-storage-1.0.jar", "/tmp/crail-storage"])  
  call(["cp", "/var/task/jars/crail-reflex-1.0.jar", "/tmp/crail-reflex"]) 
  call(["cp", "/var/task/conf/test-1mb.data", "/tmp/test-1MB"]) 

  time.sleep(20)
  
  socket = crail.connect()
  
  print "Talk to dispatcher..."
  src_filename = "/tmp/crail-reflex"
  dst_filename = "/dsttest-test-reflex2.data"
  ticket = 1001
  print "Try PUT..."
  start = time.time()
  crail.put(socket, src_filename, dst_filename, ticket)
  end = time.time()
  print "Execution time for single PUT: ", (end-start) * 1000000, " us\n"
  
  time.sleep(1)
  src_filename = "/dsttest-test-reflex2.data"
  dst_filename = "/tmp/crail-reflex-2"
  print "Now GET..."
  start = time.time()
  crail.get(socket, src_filename, dst_filename, ticket)
  end = time.time()
  print "Execution time for single GET: ", (end-start) * 1000000, " us\n"

  
  time.sleep(1)
  call(["ls", "-al", "/tmp/"])
  
  src_filename = "/dsttest-test-reflex2.data"
  print "Now DEL..."
  start = time.time()
  crail.delete(socket, src_filename, ticket)
  end = time.time()
  print "Execution time for single GET: ", (end-start) * 1000000, " us\n"

  exit(0)

  src_filename = "/tmp/test-1MB"
  dst_filename = "/test---1MB.data"
  ticket = 2000
  print "Try PUT..."
  start = time.time()
  crail.put(socket, src_filename, dst_filename, ticket)
  end = time.time()
  print "Execution time for 1MB PUT: ", (end-start) * 1000000, " us\n"
  
  src_filename = "/test---1MB.data"
  NUM_RUNS = 100
  start = time.time()
  for i in range(0,NUM_RUNS):
    dst_filename = "/tmp/dst-1MB-" + str(i)
    crail.get(socket, src_filename, dst_filename, ticket)
  end = time.time()
  print "Avg throughput for 1MB GET: ", NUM_RUNS*1048676*8/(end-start)/1000000, " Mb/s\n"

  return
