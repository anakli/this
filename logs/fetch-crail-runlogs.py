#!/usr/bin/env python

import os
import sys
import crail
import time

datadir = sys.argv[1]
netstat_dir= os.path.join(datadir, "netstats")

if not os.path.exists(datadir):
    os.makedirs(datadir)
    os.makedirs(netstat_dir)

#r = redis.StrictRedis(host=os.environ['REDIS_HOSTADDR'], port=6379, db=0)
crail.launch_dispatcher("/home/ubuntu/crail/crail-deployment/crail-1.0")
time.sleep(10)
socket = crail.connect()
ticket = 1000




#FIXME: get list of reqids
#runlog_keys = r.keys(pattern="video-lambda-logs*")
with open('crail-runlog-reqids.txt', 'r') as idfile:
  for line in idfile:
    reqid = line.replace('\n', '')
    logfile = "/video-lambda-logs/" + reqid
    crail.get(socket, logfile, datadir + "/" + reqid, ticket) 
    netstatFile = "/video-lambda-logs/netstats-" + reqid
    crail.get(socket, logfile, netstat_dir + "/" + reqid, ticket) 

