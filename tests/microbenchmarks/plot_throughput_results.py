import numpy as np
import matplotlib.pyplot as plt

N = 3

plt.rcParams.update({'font.size': 22})
plt.rcParams['errorbar.capsize'] = 2


# with 1MB requests

s3_put_1KB = [0.29, 0.26, 0.29 ]
s3_getobject_1KB = [0.58, 0.52, 0.59]

s3_put_10KB = [1.5, 1.7, 1.5, 1.5]
s3_getobject_10KB = [3.9, 4, 3.75, 4.9 ]

s3_put_100KB = [22.9, 21.7, 17.8,  21.1]
s3_getobject_100KB = [58.4, 39.5, 48.3, 48.8 ]

s3_put_1MB = [74,78,74,76,79, 65, 67, 81, 76, 80, 81 , 87, 75] #Mb/s
#s3_get_1MB = [145,86,119,117,129] # Mb/s
s3_getobject_1MB = [227,340,432, 394, 348, 351, 279, 336] # Mb/s

s3_put_10MB = [152, 140 , 165, 140, 120, 130, 147, 158, 172, 146, 163, 169] #Mb/s
#s3_getdownload_10MB = [463, 450, 460, 490] # Mb/s
#s3_getobject_10MB = [650, 722, 720, 599, 576, 518, 521, 511, 467, 494] # Mb/s
s3_getobject_10MB = [650, 620, 599, 576, 518, 521, 511, 467, 494] # Mb/s

# with 100MB requests
s3_put_100MB = [223,280,305,195,151,267, 341, 341, 330, 329 ] #Mb/s
#s3_get_100MB = [514,499,514,513, 500,513] # Mb/s
s3_getobject_100MB = [468, 495,470, 488, 509, 664, 659 ] # Mb/s

# with 1GB requests
#s3_put_1GB = [270, 195, 332, 216, 182] #Mb/s
#s3_get_1GB = [513, 510, 512, 512, 496] # Mb/s -- only get_object works (otherwise disk error)

#3x cluster of c4.8xlarge (3 shards, no replicas)
rediscluster_put_1MB = [ 614, 490, 551, 551, 551] #Mb/s 613
rediscluster_get_1MB = [ 614, 490, 552, 552, 552] # Mb/s 614

rediscluster_put_100MB = [484, 484, 484, 484, 497] #Mb/s
rediscluster_get_100MB = [486, 486, 485, 486, 507] # Mb/s

rediscluster_put_1GB = [] #TTL exhausted error #Mb/s
rediscluster_get_1GB = [] # Mb/s

#c4.8xlarge

redis_put_1KB = [29,28, 26 , 29, 31 ] #Mb/s
redis_get_1KB = [41,40.4, 40.8, 39, 40  ] # Mb/s

redis_put_10KB = [202,219, 220] #Mb/s
redis_get_10KB = [251,259, 267] # Mb/s

redis_put_100KB = [609,574, 705, 577,653] #Mb/s
redis_get_100KB = [615,609, 719, 748,655 ] # Mb/s

redis_put_1MB = [645, 646, 550, 618, 618 ] #Mb/s
redis_get_1MB = [655, 655, 552, 623, 623] # Mb/s

redis_put_10MB = [650, 594, 593, 648 ] #Mb/s #FIXME: placeholder
redis_get_10MB = [650, 500, 593, 728] # Mb/s #FIXME: placeholder

redis_put_100MB = [549, 599, 494, 680] #Mb/s
redis_get_100MB = [551, 561, 551, 690 ] # Mb/s

#redis_put_1GB = [] #TTL exhausted error #Mb/s
#redis_get_1GB = [] # Mb/s

#crail_put_1KB = [5, 5.05, 5.1 ] #5000 trials
crail_put_1KB = [11.9, 12, 11.5, 11.6, 11.5] #with nodelay #5000 trials
crail_get_1KB = [18.3, 17.8, 18.9, 15.6, 14.9]

crail_put_10KB = [108,96, 105, 83 ]
crail_get_10KB = [132,126, 134, 96 ]

crail_put_100KB = [637,632, 632, 635, 664]
crail_get_100KB = [653, 653, 657, 643, 656]

crail_put_1MB = [555, 672, 549, 669, 605, 608, 630]
crail_get_1MB = [554, 576, 502, 677, 616, 616, 643]

crail_put_10MB = [621, 508, 638, 635, 610] 
crail_get_10MB = [620, 514, 643, 643, 610] 

crail_put_100MB = [622, 506, 620]
crail_get_100MB = [ 632, 507, 633]

crail_put_1GB = [] # no space on device
crail_get_1GB = [] # no space on device


x = [1024, (1024*8), (1024*128), (1024*1024), (1024*1024*8), (1024*1024*128)]

s3_puts = (s3_put_1KB, s3_put_10KB, s3_put_100KB, s3_put_1MB, s3_put_10MB, s3_put_100MB)
s3_gets = (s3_getobject_1KB, s3_getobject_10KB, s3_getobject_100KB, s3_getobject_1MB, s3_getobject_10MB, s3_getobject_100MB)
s3_puts_mean = [np.mean(i) for i in s3_puts]
s3_gets_mean = [np.mean(i) for i in s3_gets]
s3_puts_p10 = [np.mean(i) - np.percentile(i,10) for i in s3_puts]
s3_gets_p10 = [np.mean(i) - np.percentile(i,10) for i in s3_gets]
s3_puts_p90 = [np.percentile(i,90) - np.mean(i) for i in s3_puts]
s3_gets_p90 = [np.percentile(i,90) - np.mean(i) for i in s3_gets]

redis_puts = (redis_put_1KB, redis_put_10KB, redis_put_100KB, redis_put_1MB, redis_put_10MB, redis_put_100MB)
redis_gets = (redis_get_1KB, redis_get_10KB, redis_get_100KB, redis_get_1MB, redis_get_10MB, redis_get_100MB)
redis_puts_mean = [np.mean(i) for i in redis_puts]
redis_gets_mean = [np.mean(i) for i in redis_gets]
redis_puts_p10 = [np.mean(i) - np.percentile(i,10) for i in redis_puts]
redis_gets_p10 = [np.mean(i) - np.percentile(i,10) for i in redis_gets]
redis_puts_p90 = [np.percentile(i,90) - np.mean(i) for i in redis_puts]
redis_gets_p90 = [np.percentile(i,90) - np.mean(i) for i in redis_gets]

crail_puts = (crail_put_1KB, crail_get_10KB, crail_get_100KB, crail_put_1MB, crail_put_10MB, crail_put_100MB)
crail_gets = (crail_get_1KB, crail_get_10KB, crail_get_100KB, crail_get_1MB, crail_get_10MB, crail_get_100MB)
crail_puts_mean = [np.mean(i) for i in crail_puts]
crail_gets_mean = [np.mean(i) for i in crail_gets]
crail_puts_p10 = [np.mean(i) - np.percentile(i,10) for i in crail_puts]
crail_gets_p10 = [np.mean(i) - np.percentile(i,10) for i in crail_gets]
crail_puts_p90 = [np.percentile(i,90) - np.mean(i) for i in crail_puts]
crail_gets_p90 = [np.percentile(i,90) - np.mean(i) for i in crail_gets]


#fig, ax = plt.figure()
fig, ax = plt.subplots(1,1, figsize=(15,8))
s3_get = ax.errorbar(x, s3_gets_mean, yerr=[s3_gets_p10, s3_gets_p90], fmt='ro-')
s3_put = ax.errorbar(x, s3_puts_mean, yerr=[s3_puts_p10, s3_puts_p90], fmt='ro--')
redis_get = ax.errorbar(x, redis_gets_mean, yerr=np.vstack([redis_gets_p10, redis_gets_p90]), fmt='bx-')
redis_put = ax.errorbar(x, redis_puts_mean, yerr=np.vstack([redis_puts_p10, redis_puts_p90]), fmt='bx--')
crail_get = ax.errorbar(x, crail_gets_mean, yerr=np.vstack([crail_gets_p10, crail_gets_p90]), fmt='d-', color='orange')
crail_put = ax.errorbar(x, crail_puts_mean, yerr=np.vstack([crail_puts_p10, crail_puts_p90]), fmt='d--', color='orange')
ax.set_xscale("log", nonposx='clip')
ax.legend((s3_get, s3_put, redis_get, redis_put, crail_get, crail_put), 
	('S3 GET', 'S3 PUT', 'Redis GET', 'RedisPUT', 'Crail-ReFlex GET', 'Crail-ReFlex PUT'), loc='upper left', fontsize='19')
ax.set_ylabel('Mb/s')
ax.set_xlabel('I/O size (bytes)')
fig.savefig("throughput-iosize-1lambda.pdf")
plt.show()
exit(0)

puts_p10 = [np.mean(i) - np.percentile(i, 10) for i in [s3_put, redis_put, crail_put]]
gets_p10 = [np.mean(i) - np.percentile(i, 10) for i in [s3_get, redis_get, crail_get]]

puts_p90 = [np.percentile(i, 90) - np.mean(i) for i in [s3_put, redis_put, crail_put]]
gets_p90 = [np.percentile(i, 90) - np.mean(i) for i in [s3_get, redis_get, crail_get]]


put_s3 = np.mean(s3_put) 
get_s3 = np.mean(s3_get) 


put_crail = np.mean(crail_put)
get_crail = np.mean(crail_get)

puts = (put_s3, put_redis, put_crail)
gets = (get_s3, get_redis, get_crail)

puts_std = (np.std(s3_put), np.std(redis_put), np.std(crail_put))
gets_std = (np.std(s3_get), np.std(redis_get), np.std(crail_get))

puts_p10 = [np.mean(i) - np.percentile(i, 10) for i in [s3_put, redis_put, crail_put]]
gets_p10 = [np.mean(i) - np.percentile(i, 10) for i in [s3_get, redis_get, crail_get]]

puts_p90 = [np.percentile(i, 90) - np.mean(i) for i in [s3_put, redis_put, crail_put]]
gets_p90 = [np.percentile(i, 90) - np.mean(i) for i in [s3_get, redis_get, crail_get]]

ind = np.arange(N)
width = 0.35

#fig, ax = plt.subplots()
fig, (ax,ax2) = plt.subplots(2, 1, sharex=True)
#rects1 = ax.bar(ind, puts, width, color = 'b', yerr=puts_std)
#rects2 = ax.bar(ind + width, gets, width, color = 'g', yerr=gets_std)
rects1 = ax.bar(ind, puts, width, color = 'b', yerr=np.vstack([puts_p10, puts_p90]))
rects2 = ax.bar(ind + width, gets, width, color = 'g', yerr=np.vstack([gets_p10, gets_p90]))

#rects1 = ax2.bar(ind, puts, width, color = 'b', yerr=puts_std)
#rects2 = ax2.bar(ind + width, gets, width, color = 'g', yerr=gets_std)
rects1 = ax2.bar(ind, puts, width, color = 'b', yerr=np.vstack([puts_p10, puts_p90]))
rects2 = ax2.bar(ind + width, gets, width, color = 'g', yerr=np.vstack([gets_p10, gets_p90]))
# add some text for labels, title and axes ticks
ax2.set_ylim(0,1000)
ax.set_ylim(40000,140000)

# hide the spines between ax and ax2
ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)

ax.set_ylabel('Latency (us)')
ax.set_title('Unloaded latency for 1KB requests')
ax2.set_xticks(ind + width / 2)
ax.set_xticklabels(('S3', 'Redis', 'Crail-ReFlex'))

ax.legend((rects1[0], rects2[0]), ('PUT', 'GET'))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')
        ax2.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.show()
