import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

plt.rcParams.update({'font.size': 24})

fig, (ax0, ax1) = plt.subplots(figsize=(15, 8), nrows=1, ncols=2)
N = 3 
ind = np.arange(N)
width = 0.8

#STAGE1
#s3_prep, redis_prep, crail_prep
#prep    = [8.2, 5.8, 6]
io_read = [0.4, 1.1, 1.1]
compute = [5.9, 6.2, 6]
io_write = [6.1, 3.2, 1.14]

breakdown = [io_read, compute, io_write]
breakdown_bottom = [[0]*len(io_read)]
tmp = [0]*len(io_read)
for i in breakdown:
    tmp = np.array(i)+np.array(tmp)
    breakdown_bottom.append(tmp)

c = ['#17becf', '#2ca02c', '#ff7f0e']
h = ['//', '.', '\\']
p = []
for i in xrange(len(breakdown)):
    print breakdown[i]
    print breakdown_bottom[i]
    #p.append(plt.bar(ind, breakdown[i], width, color=c[i], bottom = breakdown_bottom[i]))
    p.append(ax0.bar(ind, breakdown[i], width, color=c[i], hatch=h[i], bottom = breakdown_bottom[i]))
    
#STAGE2
#s3_prep, redis_prep, crail_prep
#prep    = [3.8, 1, 2.5]
io_read = [1.9, 0.22, 1.3]
compute = [4.8, 4.6, 4.4]
io_write = [0.15, 0.002, 0.02]

breakdown = [io_read, compute, io_write]
breakdown_bottom = [[0]*len(io_read)]
tmp = [0]*len(io_read)
for i in breakdown:
    tmp = np.array(i)+np.array(tmp)
    breakdown_bottom.append(tmp)

#c = ['b', 'g', 'r']
c = ['#17becf', '#2ca02c', '#ff7f0e']
h = ['//', '.', '\\']
p = []
for i in xrange(len(breakdown)):
    print breakdown[i]
    print breakdown_bottom[i]
    #p.append(plt.bar(ind, breakdown[i], width, color=c[i], bottom = breakdown_bottom[i]))
    p.append(ax1.bar(ind, breakdown[i], width, color=c[i], hatch = h[i], bottom = breakdown_bottom[i]))
    
ax0.set_ylabel('Average Time per Lambda (s)')
for ax in (ax0, ax1):
    ax.set_xticks(ind)
    ax.set_xticklabels(('S3', 'Redis', 'Crail-ReFlex'))
    #ax.legend((p1[0], p1_1[0], p0_2[0], p1_2[0], p2_2[0]), ('Input/Ouput','Compute','S3 R/W','Redis R/W','Pocket-Flash R/W'))
    
l = ('I/O Read', 'Compute', 'I/O Write')
ax1.legend((p[0][0], p[1][0], p[2][0]), (l), loc='upper right', ncol=1, fontsize=20)
ax0.set_title("Stage 1: Decode frames")
ax1.set_title("Stage 2: MXNET classification")
ax1.set_ylim(0,13)

#plt.tight_layout()
plt.show()

