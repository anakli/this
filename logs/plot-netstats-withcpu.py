#!/usr/bin/env python

import os
import sys
import numpy as np 
from io import StringIO 
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker


datadir = sys.argv[1]
netstat_dir = os.path.join(datadir, "netstats")
rxfilename = "rxstats.txt"
txfilename = "txstats.txt"
cpufilename = "cpustats.txt"


rxstats = open(os.path.join(netstat_dir, rxfilename), 'r')
txstats = open(os.path.join(netstat_dir, txfilename), 'r')
cpustats = open(os.path.join(netstat_dir, cpufilename), 'r')

i = 0
xmax = 0
xmin = 0
ytotal = None
DURATION = 600 #15
for line in rxstats:
	data = np.loadtxt(StringIO(unicode(line)), delimiter='\t') 
	start_time = int(data[1])
	if i == 0 :
		xmin = start_time
		xmax = xmin + DURATION
 	i += 1
	#print data
	x = np.array(range(start_time, start_time + len(data) - 2))
	y = np.delete(data, [0,1])
	#plt.fill_between(x, y_prev, y, facecolor="#CC6666", alpha=.7)
	#y_prev = y
	
	#plt.plot(x,y)
	padzeros = x[0] - xmin
	if padzeros > 0:
		y = np.pad(y, (padzeros,0), "constant", constant_values=(0,0))
	padend = xmax - x[-1]
	if padend > 0:
		y = np.pad(y, (0,padend), "constant" , constant_values=(0,0))
	if ytotal is not None:
		ytotal = np.row_stack((ytotal,y))
	else:
		ytotal = y
		#ytotal = np.row_stack((np.zeros(DURATION+1),y))
	
x = range(0, xmax - xmin +1)
ycum = np.cumsum(ytotal, axis=0)
fig = plt.figure()
ax = fig.add_subplot(111)
scale_y = 1e9
BYTES_TO_BITS=8
ycum = ycum * 8
#ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*BYTES_TO_BITS/scale_y))
#ax.yaxis.set_major_formatter(ticks_y)
ax.plot(x, np.transpose(ycum))

ax.set_xlabel("Time (s)")
ax.set_ylabel("Cumulative Gb/s")
ax.set_title("RX network utilization")

rxstats.close()


i = 0
xmax = 0
xmin = 0
ytotal = None
for line in txstats:
	data = np.loadtxt(StringIO(unicode(line)), delimiter='\t') #, np.array(line)
	start_time = int(data[1])
	if i == 0 :
		xmin = start_time
		xmax = xmin + DURATION
 	i += 1
	x = np.array(range(start_time, start_time + len(data) - 2))
	y = np.delete(data, [0,1])
	#plt.fill_between(x, y_prev, y, facecolor="#CC6666", alpha=.7)
	#y_prev = y
	
	#plt.plot(x,y)
	padzeros = x[0] - xmin
	if padzeros > 0:
		y = np.pad(y, (padzeros,0), "constant", constant_values=(0,0))
	padend = xmax - x[-1]
	if padend > 0:
		y = np.pad(y, (0,padend), "constant" , constant_values=(0,0))

	if ytotal is not None:
		ytotal = np.row_stack((ytotal,y))
	else:
		ytotal = y
		#ytotal = np.row_stack((np.zeros(DURATION+1),y))
	
x = range(0, xmax - xmin +1)
ycum = np.cumsum(ytotal, axis=0)
fig = plt.figure()
ax = fig.add_subplot(111)
scale_y = 1e9
BYTES_TO_BITS=8
ycum = ycum * 8
#ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*BYTES_TO_BITS/scale_y))
#ax.yaxis.set_major_formatter(ticks_y)
ax.plot(x, np.transpose(ycum))

ax.set_xlabel("Time (s)")
ax.set_ylabel("Cumulative Gb/s")
ax.set_title("TX network utilization")

txstats.close()


i = 0
xmax = 0
xmin = 0
ytotal = None
ylist = []
for line in cpustats:
	data = np.loadtxt(StringIO(unicode(line)), delimiter='\t') #, np.array(line)
	start_time = int(data[1])
	if i == 0 :
		xmin = start_time
		xmax = xmin + DURATION
 	i += 1
	x = np.array(range(start_time, start_time + len(data) - 2))
	y = np.delete(data, [0,1])

        padzeros = x[0] - xmin
	padend = xmax - x[-1] + padzeros
	if padend > 0:
		y = np.pad(y, (0,padend), "constant" , constant_values=(0,0))
	if ytotal is not None:
		ytotal = np.row_stack((ytotal,y))
	else:
		ytotal = y
	ylist.append(y)

x = range(0, xmax - xmin +1)

ycum = np.cumsum(ytotal, axis=0)
yind = np.array(ylist)
fig = plt.figure()
ax = fig.add_subplot(111)
scale_y = 1#1e9
BYTES_TO_BITS=1#8
ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*BYTES_TO_BITS/scale_y))
ax.yaxis.set_major_formatter(ticks_y)

ax.plot(np.transpose(yind), '.')

ax.set_xlabel("Time (s)")
ax.set_ylabel("CPU Utilization (%)")


#ax.set_title("CPU utilization" + " ("+str(n)+" "+worker+")")
ax.set_title("CPU utilization")


plt.show()
cpustats.close()
