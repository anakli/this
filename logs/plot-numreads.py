#!/usr/bin/env python

import os
import sys
import numpy as np
from io import StringIO 
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker


#python plot-numreads.py gg-cmake-crail-i3.4xl-2node-logops-100lambdas-localparseall gg-mosh-crail-i3.4xl-2node-logops-100lambdas-localputparseall

plt.rcParams.update({'font.size': 24})

opfile1 = open(os.path.join(sys.argv[1], "netstats/ops.txt"), 'r')
opfile2 = open(os.path.join(sys.argv[2], "netstats/ops.txt"), 'r')

i = 0
read_times = {}
write_times = {}
for line in opfile1:
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

#fig, ax = plt.subplots(figsize=(15, 8))
#n_bins = len(time_to_first_read)
#n, bins, patches = ax.hist(time_to_first_read, n_bins, normed=1, histtype='step',
#                           cumulative=True, label='gg-cmake', linewidth=3)
                           #cumulative=True, label='video-analytics', linewidth=3)
#patches[0].set_xy(patches[0].get_xy()[:-1])
#n, bins, patches = ax.hist(object_lifetime, n_bins, normed=1, histtype='step',
#                           cumulative=True, label='gg-cmake-lifetime', linewidth=3)
#patches[0].set_xy(patches[0].get_xy()[:-1])

#ax.legend(loc='upper left')
#ax.set_xlabel('Time to first read (seconds)')
#ax.set_xlim(1,max(videox)+1000)
#ax.set_xlim(10,10e8)
#ax.set_ylim(0,1)
#ax.set_ylabel('CDF')


fig, ax2 = plt.subplots(figsize=(15, 8))
n_bins = len(rd_access_freq)
n, bins, patches = ax2.hist(rd_access_freq, n_bins, normed=1, histtype='step',
                           cumulative=True, label='gg-cmake', linewidth=3)
patches[0].set_xy(patches[0].get_xy()[:-1])

i = 0
read_times = {}
write_times = {}
for line in opfile2:
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

n, bins, patches = ax2.hist(rd_access_freq, n_bins, normed=1, histtype='step',
                           cumulative=True, label='gg-mosh', linewidth=3)
                           #cumulative=True, label='video-analytics', linewidth=3)
patches[0].set_xy(patches[0].get_xy()[:-1])

ax2.legend(loc='lower right')
ax2.set_xlabel('Number of reads per object')
#ax.set_xlim(1,max(videox)+1000)
#ax.set_xlim(10,10e8)
ax2.set_ylim(0,1)
ax2.set_ylabel('CDF')

plt.tight_layout()
plt.savefig("numreads-gg-cdf.pdf")
plt.show()




