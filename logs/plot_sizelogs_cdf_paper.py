#!/usr/bin/env python

import os
import sys
import numpy as np
import matplotlib.pyplot as plt


# on scanne-new instance : python plot_sizelogs_cdf_paper.py video1-360p-50batch-crail-1node-jan27 gg-cmake-lambda100-sizelogs pywren_filesize_100GB_250workers.txt
#python plot_sizelogs_cdf_paper.py video1-360p-50batch-crail-1node-jan27 gg-cmake-lambda100-sizelogs sizes_100GB_500workers
#python plot_sizelogs_cdf_paper.py video3-res4-100batch1-10batch2-sizelogs  gg-cmake-lambda100-sizelogs pywren_filesize_100GB_250workers.txt
plt.rcParams.update({'font.size': 24})




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
                           cumulative=True, label='gg cmake', linewidth=3)
patches[0].set_xy(patches[0].get_xy()[:-1])


data_points = []
headers = []

datadir = sys.argv[1]
datadir = os.path.join(datadir, 'sizelogs')
infiles = {}
file_sizes = []
for logfile in os.listdir(datadir):
    path = os.path.join(datadir, logfile)

    if logfile in "netstats":
	continue
    #print "*******" + path + "********"
    with open(path, "r") as log:
        data = eval(log.read())
        point =  [] #[data['started']]
        name  = []
        name += [x[0] for x in data['sizelog']]
        point += [x[1] for x in data['sizelog']]
        data_points += [point]
        
        for x in range(0,len(point)):
            infile_shorthash = name[x][name[x].find("'")+1:name[x].find("'")]
            infile_size = int(point[x])
            infiles[infile_shorthash] = infile_size
            #print infile_shorthash + " --> " + " %d" % infile_size
            file_sizes.append(infile_size)

        #if not headers:
        #    headers += ["start"]
        #    headers += [x[0] for x in data['timelog']]

data_points.sort(key=lambda x: x[1])

#fig, ax = plt.subplots(figsize=(8, 4))
x = infiles.values() 
x = file_sizes
#print x
videox = x
#x[:] = [i / 1024 for i in x] #KB
n_bins = 8000000 #len(x)
#print len(x)
n, bins, patches = ax.hist(x, n_bins, normed=1, histtype='step',
                           cumulative=True, label='video analytics', linewidth=3, linestyle='--')
patches[0].set_xy(patches[0].get_xy()[:-1])


pywren_filesizes = open(sys.argv[3], 'r').readlines()
pywren_filesizes = [int(x.strip()) for x in pywren_filesizes] 
n, bins, patches = ax.hist(pywren_filesizes, n_bins, normed=1, histtype='step', cumulative=True, label='sort100GB', linewidth=3, linestyle=':')
patches[0].set_xy(patches[0].get_xy()[:-1])
datadir = sys.argv[1]
datadir = os.path.join(datadir, 'sizelogs')



#ax.legend(loc='lower right')
ax.legend(loc='upper left')
#ax.set_title('Data file size distribution')
ax.set_xscale('log') #,nonposx='clip')
ax.set_xlabel('I/O size (bytes)')
#ax.set_xlim(1,max(videox)+1000)
ax.set_xlim(10,10e8)
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
