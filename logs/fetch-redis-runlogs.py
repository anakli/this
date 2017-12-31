#!/usr/bin/env python

import os
import sys
import redis

datadir = sys.argv[1]
netstat_dir= os.path.join(datadir, "netstats")

if not os.path.exists(datadir):
    os.makedirs(datadir)
    os.makedirs(netstat_dir)

r = redis.StrictRedis(host=os.environ['REDIS_HOSTADDR'], port=6379, db=0)
runlog_keys = r.keys(pattern="video-lambda-logs*")

for key in runlog_keys:
    if "netstats" in key:
    	f = open(os.path.join(netstat_dir,key.split("video-lambda-logs/")[1]), 'w+')
    else:	
    	f = open(os.path.join(datadir,key.split("video-lambda-logs/")[1]), 'w+')
    f.write(r.get(key))


