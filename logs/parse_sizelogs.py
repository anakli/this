#!/usr/bin/env python

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 20})

datadir = sys.argv[1]
datadir = os.path.join(datadir, 'sizelogs')

data_points = []
headers = []

infiles = {}
file_sizes = []
for logfile in os.listdir(datadir):
    path = os.path.join(datadir, logfile)

    if logfile in "netstats":
	continue
    print "*******" + path + "********"
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
            print infile_shorthash + " --> " + " %d" % infile_size
            file_sizes.append(infile_size)

        #if not headers:
        #    headers += ["start"]
        #    headers += [x[0] for x in data['timelog']]

data_points.sort(key=lambda x: x[1])

fig, ax = plt.subplots(figsize=(8, 4))
x = infiles.values() 
x = file_sizes
print x
x[:] = [i / 1024 for i in x] #KB
n_bins = 8000000 #len(x)
print len(x)
n, bins, patches = ax.hist(x, n_bins, normed=1, histtype='step',
                           cumulative=True, label='video analytics')



# gg data : mosh-ana-lambda100-sizelogs
datadir = sys.argv[2]

file_sizes = []
for logfile in os.listdir(datadir):
    path = os.path.join(datadir, logfile)

    if logfile in "netstats":
	continue
    print "*******" + path + "********"
    with open(path, "r") as log:
        data = eval(log.read())
        point =  [] #[data['started']]
        name  = []
        name += [x[0] for x in data['timelog']]
        point += [x[1] for x in data['timelog']]
        data_points += [point]
        
        for x in range(0,len(point)):
            infile_shorthash = name[x][name[x].find("'")+1:name[x].find("'")]
            infile_size = int(point[x])
            infiles[infile_shorthash] = infile_size
            print infile_shorthash + " --> " + " %d" % infile_size
            file_sizes.append(infile_size)

#x = [ int(i) for i in file_sizes if i.isdigit()] 
#x = filter( lambda i: i > 0, x)
x = file_sizes
x[:] = [i / 1024 for i in x] #KB
#print "infile size KBs is: ", sorted(x)
n_bins = 8000000
n, bins, patches = ax.hist(x, n_bins, normed=1, histtype='step',
                           cumulative=True, label='gg-mosh')
patches[0].set_xy(patches[0].get_xy()[:-1])

ax.legend(loc='lower right')
#ax.set_title('Data file size distribution')
ax.set_xscale('log') #,nonposx='clip')
ax.set_xlabel('I/O size (KB)')
ax.set_xlim(1,max(x))
ax.set_ylim(0,1)
ax.set_ylabel('CDF')

plt.show()
#T0 = data_points[0][0]

#for d in data_points:
#    d[0] = d[0] - T0
#    d.append(sum(d))

#print("\t".join(["#"] + headers))
#for i, d in enumerate(data_points):
#    print("\t".join([str(i)] + [str(x) for x in d]))
