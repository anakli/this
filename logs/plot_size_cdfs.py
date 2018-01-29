#!/usr/bin/env python

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

filename = sys.argv[1]

data_points = []
headers = []

with open(filename, "r") as log:
    data = log.readlines()


infile_sizes = []
outfile_sizes = []

for line in data:
    linetype = line.split(": ")
    if "infiles_size" in linetype[0]:
       infile_sizes += linetype[1].split(", ") 
    if "output_size" in linetype[0]:
        outfile_sizes.append(int(linetype[1].strip()))

#datadir = sys.argv[2]
#download_sizes = []

#for logfile in os.listdir(datadir):
#    path = os.path.join(datadir, logfile)
#
#    with open(path, "r") as log:
#        data = eval(log.read())
#        download_sizes += data['timelog']
        

#plot CDF
fig, ax = plt.subplots(figsize=(8, 4))
x = [ int(i) for i in infile_sizes if i.isdigit()] 
x = filter( lambda i: i > 0, x)
x[:] = [i / 1024 for i in x] #KB
#print "infile size KBs is: ", sorted(x)
n_bins = 1000000
print len(x)
o = outfile_sizes #[ int(i) for i in outfile_sizes if i.isdigit() ] 
o[:] = [i / 1024 for i in o] #KB
#d = [ int(i) for i in download_sizes if i.isdigit()] 
#d = download_sizes
#d[:] = [i / 1024 for i in d] #KB


n, bins, patches = ax.hist(x, n_bins, normed=1, histtype='step',
                           cumulative=True, label='gg-infiles')
patches[0].set_xy(patches[0].get_xy()[:-1])
n, bins, patches = ax.hist(o, n_bins, normed=1, histtype='step',
                           cumulative=True, label='gg-outputs')
patches[0].set_xy(patches[0].get_xy()[:-1])
#n, bins, patches = ax.hist(d, n_bins, normed=1, histtype='step',
#                           cumulative=True, label='gg-downloaded-infiles')
#patches[0].set_xy(patches[0].get_xy()[:-1])
ax.legend(loc='lower right')
ax.set_title('mosh data size distribution')
ax.set_xscale('log') 
ax.set_xlabel('Input File size (KB)')
ax.set_xlim(1,max(x))
ax.set_ylim(0,1)
ax.set_ylabel('CDF')

plt.show()
