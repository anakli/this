#!/usr/bin/env python

import os
import sys
import numpy as np
from io import StringIO 
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 24})

#python parse-ops.py mxnet-video3-res4-pocket-2node-i3.4xl-100batch1-20batch2-logops-REDO gg-cmake-crail-i3.4xl-2node-logops-100lambdas-localparseall-redo/netstats/ops.txt

datadir = sys.argv[1]
datadir1 = datadir + "_stage1"
datadir2 = datadir + "_stage2"
netstat_dir1 = os.path.join(datadir1, "netstats")
netstat_dir2 = os.path.join(datadir2, "netstats")
opfilename = "ops.txt"

op_data_points = []
headers = []

for netstat_dir in [netstat_dir1, netstat_dir2]:
	for logfile in os.listdir(netstat_dir):
	    path = os.path.join(netstat_dir, logfile)

	    if "rxstats" in logfile:
		continue
	    if "txstats" in logfile:
		continue
	    if "cpustats" in logfile:
		continue
	    if "ops" in logfile:
		continue
	
	    with open(path, "r") as log:
	        data = eval(log.read())
	        oppoint = []
	        oppoint += [x + "\n" for x in data['ops']]
	        op_data_points += oppoint
	        op_data_points += "\n"
	
	        #if not headers:
	        #    headers += ["start"]
	        #    headers += [x for x in data['ops']]
	
opfile = open(os.path.join(netstat_dir1, opfilename), 'w')
for i, d in enumerate(op_data_points):
    opfile.write(str(op_data_points[i]))

opfile.close()

opfile = open(os.path.join(netstat_dir1, opfilename), 'r')

i = 0
read_times = {}
write_times = {}
for line in opfile:
	#data = np.loadtxt(StringIO(unicode(line)), delimiter=' ') 
	data = line.split(" ")
	
	if len(data) == 1:
		continue

	time = data[0]
	op = data[1]
	key = data[2].split("\n")[0]

        if "GET" in op:
		if key not in read_times.keys():
			read_times[key] = []
		read_times[key].append(time)
	elif "PUT" in data[1]:
		if key not in write_times.keys():
			write_times[key] = []
		write_times[key].append(time)


#print read_times
#print write_times

time_to_first_read = []
object_lifetime = []
rd_access_freq = []
for key, value in write_times.iteritems():
	if len(value) > 1:
		print "ERROR:" , key, value
	if key in read_times.keys():	
		time_to_first_read.append(float(read_times[key][0]) - float(value[0]))
		object_lifetime.append(float(read_times[key][-1]) - float(value[0]))
		rd_access_freq.append(len(read_times[key]))

print "Avg time to first read: ", sum(time_to_first_read)/len(time_to_first_read), " seconds"
print "Avg object lifetime:    ", sum(object_lifetime)/len(object_lifetime), "seconds"
print "Avg rd access freq:     ", sum(rd_access_freq)/len(rd_access_freq)

fig, ax = plt.subplots(figsize=(15, 8))
n_bins = len(time_to_first_read)
n, bins, patches = ax.hist(time_to_first_read, n_bins, normed=1, histtype='step',
                           cumulative=True, label='video-analytics__object-lifetime', linewidth=3)
patches[0].set_xy(patches[0].get_xy()[:-1])


opfile = open(sys.argv[2], 'r')

i = 0
read_times = {}
write_times = {}
for line in opfile:
	#data = np.loadtxt(StringIO(unicode(line)), delimiter=' ') 
	data = line.split(" ")
	
	if len(data) == 1:
		continue

	time = data[0]
	op = data[1]
	key = data[2].split("\n")[0]

        if "GET" in op:
		if key not in read_times.keys():
			read_times[key] = []
		read_times[key].append(time)
	elif "PUT" in data[1]:
		if key not in write_times.keys():
			write_times[key] = []
		write_times[key].append(time)


#print read_times
#print write_times

time_to_first_read = []
object_lifetime = []
rd_access_freq = []
for key, value in write_times.iteritems():
	if len(value) > 1:
		print "ERROR:" , key, value
	if key in read_times.keys():	
		time_to_first_read.append(float(read_times[key][0]) - float(value[0]))
		object_lifetime.append(float(read_times[key][-1]) - float(value[0]))
		rd_access_freq.append(len(read_times[key]))

print "Avg time to first read: ", sum(time_to_first_read)/len(time_to_first_read), " seconds"
print "Avg object lifetime:    ", sum(object_lifetime)/len(object_lifetime), "seconds"
print "Avg rd access freq:     ", sum(rd_access_freq)/len(rd_access_freq)

n_bins = len(time_to_first_read)
n, bins, patches = ax.hist(object_lifetime, n_bins, normed=1, histtype='step',
                           cumulative=True, label='gg-cmake__object-lifetime', linewidth=3, color="#ff7f0e" )
patches[0].set_xy(patches[0].get_xy()[:-1])
n, bins, patches = ax.hist(time_to_first_read, n_bins, normed=1, histtype='step',
                           cumulative=True, label='gg-cmake__time-to-first-read', linewidth=3, linestyle=':', color="#ff7f0e")
                           #cumulative=True, label='video-analytics', linewidth=3)
patches[0].set_xy(patches[0].get_xy()[:-1])



ax.legend(loc='lower right')
ax.set_xlabel('Time (seconds)')
#ax.set_xlim(1,max(videox)+1000)
#ax.set_xlim(10,10e8)
ax.set_ylim(0,1)
ax.set_ylabel('CDF')




#plt.title("Video analytics object lifetime and time to first read")

plt.tight_layout()
plt.savefig("object-lifetime-cdf.pdf")

plt.show()
opfile.close()



