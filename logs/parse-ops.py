#!/usr/bin/env python

import os
import sys
import numpy as np
from io import StringIO 
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

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
	
	    print logfile
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

plt.plot(range(0,len(time_to_first_read)), time_to_first_read, '.')
plt.plot(range(0,len(object_lifetime)), object_lifetime, '.')
plt.title("Video analytics object lifetime and time to first read")

plt.tight_layout()
plt.savefig(os.path.join(netstat_dir2,"ops.pdf"))

plt.show()
opfile.close()



