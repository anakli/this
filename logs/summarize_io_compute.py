#!/usr/bin/env python

import numpy as np
import pandas as pd
import os
import sys


filename = sys.argv[1]
data = pd.read_csv(filename, sep="\t", header=None)
data.columns = [ "worker", "start-time", "fetch-decoder", "fetch-deps", "execute", "upload-outfile", "cleanup", "end-time" ]
#data.columns = [ "worker", "start-time", "disk-write", "copy-executables", "fetch-deps", "execute", "check-outfile", "upload-outfile", "end-time" ]

#print "upload times:\n" , data.loc[:,"upload-outfile"]
#print "fetch times:\n" , data.loc[:,"fetch-deps"]
fetchdec= data["fetch-decoder"].sum()
fetch = data["fetch-deps"].sum()
compute = data["execute"].sum()
upload = data["upload-outfile"].sum() + data["cleanup"].sum()
total = fetchdec + fetch + compute + upload
io_total  = fetchdec + fetch + upload
io_total_perc = io_total/total * 100
compute_total_perc = compute/total * 100

print "Total fetch decoder time:" , data["fetch-decoder"].sum(), " (", fetchdec/total * 100, "%)"
print "Total fetch time:" , data["fetch-deps"].sum(), " (", fetch/total * 100, "%)"
print "Total exec time:" , data["execute"].sum() , " (", compute/total * 100, "%)"
print "Total upload time:" , data["upload-outfile"].sum() + data["cleanup"].sum(), " (", upload/total * 100, "%)"
print "Total time: ", total
print "Total I/O: ", io_total_perc, "% Total compute: ", compute_total_perc, "%"
print "Total job runtime: ", data["end-time"].iloc[-1] , "(last) and ", data["end-time"].max(), " (max) and ", data["end-time"].mean(), " (avg)"
