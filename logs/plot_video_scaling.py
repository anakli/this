#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


plt.style.use('default')
plt.rcParams.update({'font.size': 24})
plt.rcParams['errorbar.capsize'] = 2

#video analytics
numFrames = 6221
#s3
b = [5, 10, 20, 30, 40, 50, 67, 80, 100, 125, 350, 500, 1000, 2000]
n = [numFrames / i for i in b]
runtime = [14, 15, 13, 8.5, 9, 7,  7, 7.6, 7,  8, 10.5, 12, 18, 34  ]
io_perc = [73, 71, 69, 65, 66, 63, 58, 58, 52, 48, 29.6, 25, 16, 11 ]

#redis
redis_b = [5, 10, 30, 80, 100, 125, 200, 350, 500, 600, 1000, 2000] #, 3000]
redis_n = [numFrames / i for i in redis_b]
redis_runtime = [210, 120, 40, 20, 18 , 14, 14, 14.5, 15, 15.2, 24, 50] #, 80 ]
redis_io_perc = [98, 97, 92, 83, 72, 63, 56, 29.4, 23, 23, 13, 7] #, 5.7] 

fig, ax1 = plt.subplots(1,1, figsize=(15,8))
#fig, ax1 = plt.subplots()
ax1.plot(n, runtime, 'b-')
ax1.plot(redis_n, redis_runtime, 'g-')
ax1.set_xlabel('# workers')
ax1.set_xscale('log', basex=10)
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('Job Runtime (s)', color='b')
ax1.tick_params('y', colors='b')
ax1.set_ylim(0, 50)

ax2 = ax1.twinx()
ax2.plot(n, io_perc, 'b--')
ax2.plot(redis_n, redis_io_perc, 'g--')
ax2.set_ylabel('IO time %', color='r')
ax2.set_ylim(0,100)
ax2.tick_params('y', colors='r')


for axis in [ax1.xaxis, ax1.yaxis]:
    axis.set_major_formatter(ScalarFormatter())
for axis in [ax2.xaxis, ax2.yaxis]:
    axis.set_major_formatter(ScalarFormatter())

fig.tight_layout()
fig.savefig("video-strong-scaling-runtime-iotime.pdf")
plt.show()

