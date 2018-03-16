#!/usr/bin/env python
from __future__ import print_function
import os
import sys

numParentLambdas = int(sys.argv[1])


logdir = "video-lambda-logs"

f1 = open("crail-logs-reqids.txt", "w")
f2 = open("crail-logs-reqids-netstats.txt", "w")

for i in range (0,numParentLambdas):
	f1.write("/" + logdir + "/lambda" + str(i) + "\n")


for i in range (0,numParentLambdas):
	f2.write("/" + logdir + "/netstats-lambda" + str(i) + "\n")
