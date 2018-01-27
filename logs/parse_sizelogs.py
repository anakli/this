#!/usr/bin/env python

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

datadir = sys.argv[1]

data_points = []
headers = []

infiles = {}

for logfile in os.listdir(datadir):
    path = os.path.join(datadir, logfile)

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

        #if not headers:
        #    headers += ["start"]
        #    headers += [x[0] for x in data['timelog']]

data_points.sort(key=lambda x: x[1])

fig, ax = plt.subplots(figsize=(8, 4))
x = infiles.values() 
x[:] = [i / 1024 for i in x] #KB
n_bins = len(x)
print len(x)
n, bins, patches = ax.hist(x, n_bins, normed=1, histtype='step',
                           cumulative=True, label='gg-mosh')
ax.legend(loc='right')
ax.set_title('Data file size distribution')
ax.set_xscale('log') #,nonposx='clip')
ax.set_xlabel('Input File size (KB)')
ax.set_xlim(0,max(x))
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
