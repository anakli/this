## Simple lambda microbenchmark for unloaded latency tests

import time
import sys
import os
import boto3
import botocore
from subprocess import call

def handler(event, context):
  #call(["ls", "-l"])
  #call(["pwd"])
  os.environ["CLASSPATH"] = "/var/task/reflex-client-1.0.jar:/var/task/reflex-client-1.0-tests.jar:/var/task/reflex-client-1.0-jar-with-dependencies.jar:/var/task/log4j.properties"
  # THROUGHPUT
  #call(["java", "-Dlog4j.configuration=file:///var/task/log4j.properties", "stanford.reflex.SimpleReflexClient", "-a", "10.0.151.74", "-k", "10000", "-b", "8", "-q", "8", "-s", "1048576"])
  #call(["java", "-Dlog4j.configuration=file:///var/task/log4j.properties", "stanford.reflex.SimpleReflexClient", "-a", "10.0.151.74", "-k", "15000", "-b", "8", "-q", "8", "-s", "1048576"])
  # LATENCY
  #call(["java", "-Dlog4j.configuration=file:///var/task/log4j.properties", "stanford.reflex.SimpleReflexClient", "-a", "10.0.151.74", "-k", "10000", "-b", "1", "-q", "1", "-s", "4096"])
  #call(["java", "-Dlog4j.configuration=file:///var/task/log4j.properties", "stanford.reflex.SimpleReflexClient", "-a", "10.0.151.74", "-k", "1", "-b", "1", "-q", "1", "-s", "4096"])
 
  # try with crail
  os.environ["CLASSPATH"] = "/var/task/jars/crail-client-1.0.jar:/var/task/crail-reflex-1.0.jar:/var/task/reflex-client-1.0-jar-with-dependencies.jar:/var/task/log4j.properties"
  os.environ["CRAIL_HOME"] = "/var/task/"
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/jre-1.8.0-openjdk.x86_64"
  call(["mkdir", "/tmp/hugepages"]) 
  call(["mkdir", "/tmp/hugepages/cache"]) 
  call(["mkdir", "/tmp/hugepages/data"]) 
  
  #call(["./bin/crail", "iobench", "-t", "write", "-f", "/test2.data", "-w", "0", "-k", "10000", "-s", "1048576", "-b", "8"]) 
  #call(["./bin/crail", "iobench", "-t", "readSequential", "-f", "/test2.data", "-w", "0", "-k", "10000", "-s", "1048576", "-b", "8"]) 
  
  call(["./bin/crail", "iobench", "-t", "write", "-f", "/test2.data", "-w", "0", "-k", "10000", "-s", "4096"]) 
  call(["./bin/crail", "iobench", "-t", "readSequential", "-f", "/test2.data", "-w", "0", "-k", "10000", "-s", "4096"]) 
  return
