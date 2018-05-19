#!/usr/bin/env python3

import os
import sys

datadir = sys.argv[1]

datadir1 = datadir + "_stage1"
datadir2 = datadir + "_stage2"

data_points = []
headers = []
io_rd_prep = []
io_rd_time = []
io_wr_time = []
compute_time = []
total_time = []
stage1_lambdas = 0
stage2_lambdas = 0


for logfile in os.listdir(datadir1):
    path = os.path.join(datadir1, logfile)

    if "netstats" in logfile:
        continue

    if "sizelogs" in logfile:
        continue

    #with open(logfile, "r") as log:
    with open(path, "r") as log:
        data = eval(log.read())
        point = [data['started']]
        io_rd_prep += [float(x[1]) if 'prepare decoder' in x[0] else 0 for x in data['timelog']]
        io_rd_time += [float(x[1]) if 'download_inputs' in x[0] else 0 for x in data['timelog']]
        compute_time += [float(x[1]) if 'combine' in x[0] else 0 for x in data['timelog']]
        io_wr_time += [float(x[1]) if 'upload' in x[0] else 0 for x in data['timelog']]
        point += [x[1] for x in data['timelog']]
	total_time += [x[1] for x in data['timelog']]
        data_points += [point]
	stage1_lambdas += 1

        if not headers:
            headers += ["start"]
            headers += [x[0] for x in data['timelog']]

io_rd_prep2 = []
io_rd_time2 = []
io_wr_time2 = []
compute_time2 = []
total_time2 = []

for logfile in os.listdir(datadir2):
    path = os.path.join(datadir2, logfile)

    if "netstats" in logfile:
        continue

    if "sizelogs" in logfile:
        continue

    #with open(logfile, "r") as log:
    with open(path, "r") as log:
        data = eval(log.read())
        point = [data['started']]
        point += [x[1] for x in data['timelog']]
        io_rd_prep2 += [float(x[1]) if 'download model' in x[0] else 0 for x in data['timelog']]
        io_rd_time2 += [float(x[1]) if 'download_inputs' in x[0] else 0 for x in data['timelog']]
        compute_time2 += [float(x[1]) if 'compute' in x[0] else 0 for x in data['timelog']]
        io_wr_time2 += [float(x[1]) if 'upload' in x[0] else 0 for x in data['timelog']]
        data_points += [point]
	total_time2 += [x[1] for x in data['timelog']]
	stage2_lambdas += 1

        if not headers:
            headers += ["start"]
            headers += [x[0] for x in data['timelog']]

data_points.sort(key=lambda x: x[0])

T0 = data_points[0][0]

for d in data_points:
    d[0] = d[0] - T0
    d.append(sum(d))

end = 0
#print("\t".join(["#"] + headers))
for i, d in enumerate(data_points):
    #print("\t".join([str(i)] + [str(x) for x in d]))
    if d[-1] > end :
        end = d[-1]

print "Video lambda runtime: ", end, "seconds (", end/60, " minutes)."
print "Stage1 lambdas: ", stage1_lambdas, "  Stage2 lambdas: ", stage2_lambdas
print "STAGE1:"
print "Prep time: ", sum(io_rd_prep), "(", sum(io_rd_prep)/sum(total_time)*100, ")"
print "Rd time: ", sum(io_rd_time), "(", sum(io_rd_time)/sum(total_time)*100, ")"
print "Compute time: ", sum(compute_time), "(", sum(compute_time)/sum(total_time)*100, ")"
print "Wr time: ", sum(io_wr_time), "(", sum(io_wr_time)/sum(total_time) * 100, ")"
print "Total IO Time: ", (sum(io_rd_time) + sum(io_wr_time))
print "       out of: ", sum(total_time), " (", (sum(io_rd_time) + sum(io_wr_time))/sum(total_time) * 100, "%)"
print "STAGE2:"
print "Prep time: ", sum(io_rd_prep2), "(", sum(io_rd_prep2)/sum(total_time2)*100, ")"
print "Rd time: ", sum(io_rd_time2), "(", sum(io_rd_time2)/sum(total_time2)*100, ")"
print "Compute time: ", sum(compute_time2), "(", sum(compute_time2)/sum(total_time2)*100, ")"
print "Wr time: ", sum(io_wr_time2), "(", sum(io_wr_time2)/sum(total_time2) * 100, ")"
print "Total IO Time: ", (sum(io_rd_time2) + sum(io_wr_time2))
print "       out of: ", sum(total_time2), " (", (sum(io_rd_time2) + sum(io_wr_time2))/sum(total_time2) * 100, "%)"

#TODO plot stacked bar plot
stage1_prep = sum(io_rd_prep) / stage1_lambdas
stage1_rd = sum(io_rd_time) / stage1_lambdas
stage1_compute = sum(compute_time) / stage1_lambdas
stage1_wr = sum(io_wr_time) / stage1_lambdas

stage2_prep = sum(io_rd_prep2) / stage2_lambdas
stage2_rd = sum(io_rd_time2) / stage2_lambdas
stage2_compute = sum(compute_time2) / stage2_lambdas
stage2_wr = sum(io_wr_time2) / stage2_lambdas

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 24})

fig, ax = plt.subplots(figsize=(15, 8))

N = 2 
ind = np.arange(N)
width = 0.5

prep    = [stage1_prep, stage2_prep]
io_read = [stage1_rd, stage2_rd]
compute = [stage1_compute, stage2_compute]
io_write = [stage1_wr, stage2_wr]

breakdown = [prep, io_read, compute, io_write]
breakdown_bottom = [[0]*len(prep)]
tmp = [0]*len(prep)
for i in breakdown:
    tmp = np.array(i)+np.array(tmp)
    breakdown_bottom.append(tmp)

c = ['b', 'r', 'y', 'g']
p = []
for i in xrange(len(breakdown)):
    print breakdown[i]
    print breakdown_bottom[i]
    p.append(plt.bar(ind, breakdown[i], width, color=c[i], bottom = breakdown_bottom[i]))
    

ax.set_ylabel('Average Time per Lambda (s)')
ax.set_xticks(ind)
ax.set_xticklabels(('Stage1', 'Stage2'))
#ax.legend((p1[0], p1_1[0], p0_2[0], p1_2[0], p2_2[0]), ('Input/Ouput','Compute','S3 R/W','Redis R/W','Pocket-Flash R/W'))
l = ('Prep time', 'I/O Read', 'Compute', 'I/O Write')
ax.legend((p[0][0], p[1][0], p[2][0], p[3][0]), (l), loc='upper right', ncol=1, fontsize=20)

plt.tight_layout()
plt.savefig("graphs/"+datadir+".pdf")

plt.show()


