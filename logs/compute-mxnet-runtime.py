#!/usr/bin/env python3

import os
import sys

datadir = sys.argv[1]

datadir1 = datadir + "_stage1"
datadir2 = datadir + "_stage2"

data_points = []
headers = []
io_rd_time = []
io_wr_time = []
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
        io_rd_time += [int(x[1]) if 'download_inputs' in x[0] else 0 for x in data['timelog']]
        io_wr_time += [int(x[1]) if 'upload' in x[0] else 0 for x in data['timelog']]
        point += [x[1] for x in data['timelog']]
	total_time += [x[1] for x in data['timelog']]
        data_points += [point]
	stage1_lambdas += 1

        if not headers:
            headers += ["start"]
            headers += [x[0] for x in data['timelog']]

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
        io_rd_time += [x[1] if 'download_inputs' in x[0] else 0 for x in data['timelog']]
        io_wr_time += [x[1] if 'upload' in x[0] else 0 for x in data['timelog']]
        data_points += [point]
	total_time += [x[1] for x in data['timelog']]
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
print "Rd time: ", sum(io_rd_time), "  Wr time: ", sum(io_wr_time)
print "Total IO Time: ", (sum(io_rd_time) + sum(io_wr_time))
print "       out of: ", sum(total_time), " (", (sum(io_rd_time) + sum(io_wr_time))/sum(total_time) * 100, "%)"
