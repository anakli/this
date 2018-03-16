#!/usr/bin/env python

import os
import sys

datadir = sys.argv[1]
netstat_dir = os.path.join(datadir, "netstats")
rxfilename = "rxstats.txt"
txfilename = "txstats.txt"
cpufilename = "cpustats.txt"

rx_data_points = []
tx_data_points = []
cpu_data_points = []
headers = []

for logfile in os.listdir(netstat_dir):
    path = os.path.join(netstat_dir, logfile)
    #print "reading file " + path
    with open(path, "r") as log:
        data = log.read()
        data = eval(data)
        rxpoint = [data['started']]
        rxpoint += [x for x in data['rx']]
        rx_data_points += [rxpoint]

        txpoint = [data['started']]
        txpoint += [x for x in data['tx']]
        tx_data_points += [txpoint]

        cpupoint = [data['started']]
        cpupoint += [x for x in data['cpu']]
        cpu_data_points += [cpupoint]
        if not headers:
            headers += ["start"]
            headers += [x for x in data['rx']]

rx_data_points.sort(key=lambda x: x[0])
tx_data_points.sort(key=lambda x: x[0])
cpu_data_points.sort(key=lambda x: x[0])

rxfile = open(os.path.join(netstat_dir, rxfilename), 'w')
for i, d in enumerate(rx_data_points):
    rxfile.write("\t".join([str(i)] + [str(x) for x in rx_data_points[i]]) + "\n")
rxfile.close()

txfile = open(os.path.join(netstat_dir, txfilename), 'w')
for i, d in enumerate(tx_data_points):
    txfile.write("\t".join([str(i)] + [str(x) for x in tx_data_points[i]]) + "\n")
txfile.close()

cpufile = open(os.path.join(netstat_dir, cpufilename), 'w')
for i, d in enumerate(cpu_data_points):
    cpufile.write("\t".join([str(i)] + [str(x) for x in cpu_data_points[i]]) + "\n")
cpufile.close()

##plot
#import numpy as np 
#from io import StringIO 
#import matplotlib.pyplot as plt
#
#rxstats = open(os.path.join(netstat_dir, rxfilename), 'r')
#txstats = open(os.path.join(netstat_dir, txfilename), 'r')
#
#y_prev = 0
#i = 0
#xmax = 0
#xmin = 0
#ytotal = None
#for line in rxstats:
#	data = np.loadtxt(StringIO(unicode(line)), delimiter='\t') #, np.array(line)
#	start_time = int(data[1])
#	if i == 0 :
#		xmin = start_time
# 	i += 1
#	x = np.array(range(start_time, start_time + len(data) - 2))
#	y = np.delete(data, [0,1])
#	#plt.fill_between(x, y_prev, y, facecolor="#CC6666", alpha=.7)
#	#y_prev = y
#	
#	plt.plot(x,y)
#	xmax = xmin + 15
#	padzeros = x[0] - xmin
#	if padzeros > 0:
#		np.pad(y, (padzeros,0), "constant", (0,0))
#	padend = xmax - x[-1]
#	if padend > 0:
#		np.pad(y, (0,padend), "constant" , (0,0))
#
#	if ytotal is not None:
#		ytotal = np.row_stack(ytotal,y)
#	else:
#		ytotal = y
#	# if x[0] < xmin: pad y by x[0]-xmin 0s
#	# if x[-1] > xmax 
#	
#x = range(0, xmax - xmin)
#y.cumsum(ytotal, axis=0)
#plt.xlabel("Time (s)")
#plt.ylabel("bytes/s")
#plt.title("RX network utilization")
#plt.show()
#
#
