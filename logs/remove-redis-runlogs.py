#!/usr/bin/env python

import redis
import os
import sys


r = redis.Redis(host=os.environ['REDIS_HOSTADDR'], port=6379)
#runlog_keys = r.delete("*")

for key in r.scan_iter('*'):
        r.delete(key)


