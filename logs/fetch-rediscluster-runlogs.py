#!/usr/bin/env python

import os
import sys
from rediscluster import StrictRedisCluster

datadir = sys.argv[1]

if not os.path.exists(datadir):
    os.makedirs(datadir)

r = StrictRedisCluster(startup_nodes=[{"host": os.environ['REDIS_HOSTADDR'], "port": "6379"}], decode_responses=False, skip_full_coverage_check=True)
runlog_keys = r.keys(pattern="video-lambda-logs*")

for key in runlog_keys:
    f = open(os.path.join(datadir,key.split("video-lambda-logs/")[1]), 'w+')
    f.write(r.get(key))
    f.close()


