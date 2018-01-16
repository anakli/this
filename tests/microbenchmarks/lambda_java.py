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

  time.sleep(20)
  
  socket = crail.connect()
  
  print "Talk to dispatcher..."
  src_filename = "/tmp/crail-reflex"
  dst_filename = "/dsttest-test-reflex.data"
  ticket = 1000
  print "Try PUT..."
  start = time.time()
  crail.put(socket, src_filename, dst_filename, ticket)
  end = time.time()
  print "Execution time for single PUT: ", (end-start) * 1000000, " us\n"
  
  #time.sleep(20)
  src_filename = "/dsttest-test-reflex.data"
  dst_filename = "/tmp/crail-reflex-2"
  print "Now GET..."
  start = time.time()
  crail.get(socket, src_filename, dst_filename, ticket)
  end = time.time()
  print "Execution time for single GET: ", (end-start) * 1000000, " us\n"
  return
