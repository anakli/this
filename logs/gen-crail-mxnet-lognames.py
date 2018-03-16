#!/usr/bin/env python
from __future__ import print_function
import os
import sys

numParentLambdas = int(sys.argv[1])
numFiles = int(sys.argv[2])

numChildLambdas = numFiles / numParentLambdas + 1

logdir = "video-lambda-logs-mxnet"

f1 = open("crail-logs-reqids-mxnet.txt", "w")
f2 = open("crail-logs-reqids-mxnet-netstats.txt", "w")

for i in range (0,numParentLambdas):
	for j in range(0, numChildLambdas):
		f1.write("/" + logdir + "/mxnetparentLambda" + str(i) + "-childLambda" + str(j) + "\n")


for i in range (0,numParentLambdas):
	for j in range(0, numChildLambdas):
		f2.write("/" + logdir + "/netstats-mxnetparentLambda" + str(i) + "-childLambda" + str(j) + "\n")
