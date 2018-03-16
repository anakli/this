#!/usr/bin/env python

import os
import sys
import crail
import time

datadir1 = sys.argv[1] + "_stage1"
datadir2 = sys.argv[1] + "_stage2"
netstat_dir1= os.path.join(datadir1, "netstats")
netstat_dir2= os.path.join(datadir2, "netstats")

if not os.path.exists(datadir1):
    os.makedirs(datadir1)
    os.makedirs(netstat_dir1)

if not os.path.exists(datadir2):
    os.makedirs(datadir2)
    os.makedirs(netstat_dir2)

#r = redis.StrictRedis(host=os.environ['REDIS_HOSTADDR'], port=6379, db=0)
p = crail.launch_dispatcher(os.environ['CRAIL_HOME'])
socket = crail.connect()
ticket = 1000




#FIXME: get list of reqids
#runlog_keys = r.keys(pattern="video-lambda-logs*")
#with open('crail-runlog-reqids.txt', 'r') as idfile:
with open('crail-logs-reqids.txt', 'r') as idfile:
  for line in idfile:
    logfile = line.replace('\n', '')
    logfile1 = logfile.replace('/video-lambda-logs/', '')
    crail.get(socket, logfile, os.path.join(datadir1,logfile1), ticket) 


with open('crail-logs-reqids-netstats.txt', 'r') as idfile:
  for line in idfile:
    logfile = line.replace('\n', '')
    logfile1 = logfile.replace('/video-lambda-logs/', '')
    crail.get(socket, logfile, os.path.join(netstat_dir1,logfile1), ticket) 

with open('crail-logs-reqids-mxnet.txt', 'r') as idfile:
  for line in idfile:
    logfile = line.replace('\n', '')
    logfile1 = logfile.replace('/video-lambda-logs-mxnet/', '')
    crail.get(socket, logfile, os.path.join(datadir2,logfile1), ticket) 


with open('crail-logs-reqids-mxnet-netstats.txt', 'r') as idfile:
  for line in idfile:
    logfile = line.replace('\n', '')
    logfile1 = logfile.replace('/video-lambda-logs-mxnet/', '')
    crail.get(socket, logfile, os.path.join(netstat_dir2,logfile1), ticket) 

crail.close(socket, ticket, p)
