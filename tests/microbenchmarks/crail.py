#######################################################
##  Python API to communicate with Crail dispatcher  ##
#######################################################

import time
import sys
import os
import socket
import struct
import errno
from subprocess import call, Popen

PORT = 2345
HOSTNAME = "localhost"
CMD_GET = 1
CMD_PUT = 0

def setup_env():
  os.environ["CLASSPATH"] = """/var/task/jars/crail-client-1.0.jar:/var/task/crail-reflex-1.0.jar:
			     /var/task/reflex-client-1.0-jar-with-dependencies.jar:
                             /var/task/log4j.properties:/var/task/jars/crail-dispatcher-1.0.jar"""
  os.environ["CRAIL_HOME"] = "/var/task/"
  os.environ["JAVA_HOME"] = "/usr/lib/jvm/jre-1.8.0-openjdk.x86_64"
  call(["mkdir", "/tmp/hugepages"]) 
  call(["mkdir", "/tmp/hugepages/cache"]) 
  call(["mkdir", "/tmp/hugepages/data"]) 
  return

def launch_dispatcher():
  setup_env()
  Popen(["java", "-cp", "/var/task/jars/*", 
	         "-Dlog4j.configuration=file:///var/task/conf/log4j.properties", 
		 "com.ibm.crail.dispatcher.CrailDispatcher"])
  return 

def connect():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOSTNAME, PORT))
  except socket.error as e:
    if e.errno == errno.ECONNREFUSED:
      print "Connection refused -- did you launch_dispatcher?"
      return None
    else:
      raise
      return None
  print "Connected to crail dispatcher." 

  return s
 
 
def pack_msg(src_filename, dst_filename, ticket, cmd):
  src_filename_len = len(src_filename) 
  dst_filename_len = len(dst_filename)
  msg_packer = struct.Struct("!iqhi" + str(src_filename_len) + "si" + str(dst_filename_len) + "s")
  msg_len = 2 + 4 + src_filename_len + 4 + dst_filename_len

  msg = (msg_len, ticket, cmd, src_filename_len, src_filename, dst_filename_len, dst_filename)
  pkt = msg_packer.pack(*msg)

  return pkt

def put(socket, src_filename, dst_filename, ticket):  
  '''
  Send a PUT request to Crail 

  :param str src_filename: name of local file containing data to PUT
  :param str dst_filename: name of file/key in Crail which writing to
  :param int ticket:       value greater than 0, unique to each connection
  :return: the Crail dispatcher response 
  '''
  pkt = pack_msg(src_filename, dst_filename, ticket, CMD_PUT) 

  socket.sendall(pkt) 
  data = socket.recv(4)

  return data

 
def get(socket, src_filename, dst_filename, ticket):  
  '''
  Send a GET request to Crail 

  :param str src_filename: name of file/key in Crail from which reading
  :param str dst_filename: name of local file where want to store data from GET
  :param int ticket:       value greater than 0, unique to each connection
  :return: the Crail dispatcher response 
  '''
  pkt = pack_msg(src_filename, dst_filename, ticket, CMD_GET) 

  socket.sendall(pkt) 
  data = socket.recv(4)

  return data

