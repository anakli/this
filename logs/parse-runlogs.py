#!/usr/bin/env python3

import os
import sys

datadir = sys.argv[1]

data_points = []
headers = []

for logfile in os.listdir(datadir):
    path = os.path.join(datadir, logfile)

    if "netstats" in logfile:
        continue

    #with open(logfile, "r") as log:
    with open(path, "r") as log:
        data = eval(log.read())
        point = [data['started']]
        point += [x[1] for x in data['timelog']]
        data_points += [point]

        if not headers:
            headers += ["start"]
            headers += [x[0] for x in data['timelog']]

data_points.sort(key=lambda x: x[0])

T0 = data_points[0][0]

for d in data_points:
    d[0] = d[0] - T0
    d.append(sum(d))

#print("\t".join(["#"] + headers))
for i, d in enumerate(data_points):
    print("\t".join([str(i)] + [str(x) for x in d]))

