#!/usr/bin/env python

from rediscluster import StrictRedisCluster
import os
import sys


r = StrictRedisCluster(startup_nodes=[{"host": os.environ['REDIS_HOSTADDR'], "port": "6379"}], decode_responses=False, skip_full_coverage_check=True)
#runlog_keys = r.delete("*")

for key in r.scan_iter('*'):
        r.delete(key)


