#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

#python plot_sizelogs_cdf_osdi18.py video3-res4-sizelogs  gg-cmake-lambda100-sizelogs pywren_filesize_100GB_250workers.txt
plt.rcParams.update({'font.size': 30})




# gg data: gg-cmake-lambda100-sizelogs
datadir = sys.argv[2]

file_sizes = []
for logfile in os.listdir(datadir):
    path = os.path.join(datadir, logfile)

    if logfile in "netstats":
	continue
    #print "*******" + path + "********"
    with open(path, "r") as log:
        data = eval(log.read())
        for x in data['timelog']:
	        file_sizes.append(x)
        
fig, ax = plt.subplots(figsize=(15, 8))
x = file_sizes
n_bins = 8000000
n, bins, patches = ax.hist(x, n_bins, normed=1, histtype='step',
                           cumulative=True, label=r'$\lambda$'.decode("utf-8")+'-cc cmake',
						   linewidth=4)
patches[0].set_xy(patches[0].get_xy()[:-1])


data_points = []
headers = []

n_bins = 8000000 #len(x)
#print len(x)
video_filesizes = open(sys.argv[1], 'r').readlines()
video_filesizes = [int(x.strip()) for x in video_filesizes] 
n, bins, patches = ax.hist(video_filesizes, n_bins, normed=1, histtype='step',
                           cumulative=True, label='video analytics', linewidth=4, linestyle='--')
patches[0].set_xy(patches[0].get_xy()[:-1])


pywren_filesizes = open(sys.argv[3], 'r').readlines()
pywren_filesizes = [int(x.strip()) for x in pywren_filesizes] 
n, bins, patches = ax.hist(pywren_filesizes, n_bins, normed=1, histtype='step', cumulative=True,
						   label='sort100GB', linewidth=4, linestyle=':')
patches[0].set_xy(patches[0].get_xy()[:-1])
datadir = sys.argv[1]
datadir = os.path.join(datadir, 'sizelogs')



#ax.legend(loc='lower right')
ax.legend(loc='upper left')
#ax.set_title('Data file size distribution')
ax.set_xscale('log') #,nonposx='clip')
ax.set_xlabel('Ephemeral Object Size (bytes)')
#ax.set_xlim(1,max(videox)+1000)
ax.set_xlim(10,10e7)
ax.set_ylim(0,1)
ax.set_ylabel('CDF')

fig.tight_layout()
fig.savefig("serverless-app-iosize-cdf.pdf")
plt.show()
#T0 = data_points[0][0]

#for d in data_points:
#    d[0] = d[0] - T0
#    d.append(sum(d))

#print("\t".join(["#"] + headers))
#for i, d in enumerate(data_points):
#    print("\t".join([str(i)] + [str(x) for x in d]))
