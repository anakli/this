import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style

plt.style.use('default')
plt.rcParams.update({'font.size': 24})
plt.rcParams['errorbar.capsize'] = 2

#~90 lambdas
gg_mosh_fetch = 15.8
gg_mosh_compute = 38.6
gg_mosh_upload = 23.1
gg_mosh_total = gg_mosh_fetch + gg_mosh_compute + gg_mosh_upload

#~500 lambdas total (but this is for 100 at a time?) 
#FIXME: compare 100max to 1000max lambda exec!
gg_openssh_fetch = 67.4
gg_openssh_compute = 42.6
gg_openssh_upload = 94.7
gg_openssh_total= gg_openssh_fetch + gg_openssh_compute + gg_openssh_upload

#~2000 lambdas (but this is for 100 at at time)
#FIXME: compare 100max to 1000max lambda exec!
gg_cmake_fetch = 278
gg_cmake_compute = 460
gg_cmake_upload = 371
gg_cmake_total = gg_cmake_fetch + gg_cmake_compute + gg_cmake_upload


names = ('gg-mosh', 'gg-openssh', 'gg-cmake')
barWidth = 0.5
r = range(0,len(names))
totals = [gg_mosh_total, gg_openssh_total, gg_cmake_total]
fetch = [gg_mosh_fetch, gg_openssh_fetch, gg_cmake_fetch]
compute = [gg_mosh_compute, gg_openssh_compute, gg_cmake_compute]
upload = [gg_mosh_upload, gg_openssh_upload, gg_cmake_upload]
fetch_p = [i / j * 100 for i,j in zip(fetch, totals)]
compute_p = [i / j * 100 for i,j in zip(compute, totals)]
upload_p = [i / j * 100 for i,j in zip(upload, totals)]

plt.bar(r, fetch_p, edgecolor='white',width=barWidth) 
plt.bar(r, compute_p, bottom=fetch_p, edgecolor='white',width=barWidth) 
plt.bar(r, upload_p, bottom=[i+j for i,j in zip(fetch_p, compute_p)],edgecolor='white',width=barWidth) 

plt.xticks(r,names)
plt.ylabel("% of total Lambda worker time")
plt.show()
exit(0)


video1_360p_batch50_fetch_decoder = 184 
video1_360p_batch50_fetch = 38
video1_360p_batch50_compute = 21
video1_360p_batch50_upload = 8
video3_4k_batch50_total = video1_360p_batch50_fetch_decoder + video1_360p_batch50_fetch + video1_360p_batch50_compute + video1_360p_batch50_upload

video3_4k_batch50_fetch_decoder = 289
video3_4k_batch50_fetch = 47
video3_4k_batch50_compute = 653
video3_4k_batch50_upload = 13
video3_4k_batch50_total = video3_4k_batch50_fetch_decoder + video3_4k_batch50_fetch + video3_4k_batch50_compute + video3_4k_batch50_upload


Total fetch decoder time: 289.498018503
Total fetch time: 47.3604879379
Total exec time: 653.193216562
Total upload time: 12.8458476067




put_crail = np.mean(crail_put_times)
get_crail = np.mean(crail_get_times)
print "PUT: ",  put_crail,  " GET: " ,  get_crail
print "PUT with no skipdir: " , np.mean(crail_put_times_noskipdir)

#putkey_crail = np.mean(crail_putkey_times)
#getkey_crail = np.mean(crail_getkey_times)

putkey_skipdir_crail = np.mean(crail_putkey_skipdir_times)
getkey_skipdir_crail = np.mean(crail_getkey_skipdir_times)

#puts = (put_s3, put_redis, put_crail, putkey_skipdir_crail)
#gets = (get_s3, get_redis, get_crail, getkey_skipdir_crail)

puts = (s3_put_times, redis_put_times, crail_putkey_skipdir_times)
gets = (s3_get_times, redis_get_times, crail_getkey_skipdir_times)
#puts = (put_s3, put_redis, put_crail)
#gets = (get_s3, get_redis, get_crail)
#puts_std = [np.std(i) for i in puts]
#gets_std = [np.std(i) for i in gets]
puts_p10 = [np.mean(i) - np.percentile(i,10) for i in puts]
gets_p10 = [np.mean(i) - np.percentile(i,10) for i in gets]
puts_p90 = [np.percentile(i,90) - np.mean(i) for i in puts]
gets_p90 = [np.percentile(i,90) - np.mean(i) for i in gets]

puts = (put_s3, put_redis, putkey_skipdir_crail)
gets = (get_s3, get_redis, getkey_skipdir_crail)

ccrail_put_times = (s3_put_times, redis_put_times, crail_put_times)
ccrail_get_times = (s3_get_times, redis_get_times, crail_get_times)

cputs = (s3_put_times, redis_put_times, crail_putkey_skipdir_times)
cgets = (s3_get_times, redis_get_times, crail_getkey_skipdir_times)
cputs_p10 = [np.mean(i) - np.percentile(i,10) for i in ccrail_put_times]
cgets_p10 = [np.mean(i) - np.percentile(i,10) for i in ccrail_get_times]
cputs_p90 = [np.percentile(i,90) - np.mean(i) for i in ccrail_put_times]
cgets_p90 = [np.percentile(i,90) - np.mean(i) for i in ccrail_get_times]

cputs = (put_s3, put_redis, put_crail)
cgets = (get_s3, get_redis, get_crail)
#puts_std = (np.std(s3_put_times), np.std(redis_put_times), np.std(crail_put_times))
#gets_std = (np.std(s3_get_times), np.std(redis_get_times), np.std(crail_get_times))

#puts_p10 = [np.mean(i) - np.percentile(i, 10) for i in [s3_put_times, redis_put_times, crail_put_times]]
#gets_p10 = [np.mean(i) - np.percentile(i, 10) for i in [s3_get_times, redis_get_times, crail_get_times]]

#puts_p90 = [np.percentile(i, 90) - np.mean(i) for i in [s3_put_times, redis_put_times, crail_put_times]]
#gets_p90 = [np.percentile(i, 90) - np.mean(i) for i in [s3_get_times, redis_get_times, crail_get_times]]

ind = np.arange(N)
width = 0.35

print puts_p10
print puts_p90

delta_puts = tuple(map(lambda x, y: x - y, cputs, puts))
delta_gets = tuple(map(lambda x, y: x - y, cgets, gets))

#fig, ax = plt.subplots()
fig, (ax,ax2) = plt.subplots(2, 1,figsize=(15,8) ,sharex=True)
#rects1 = ax.bar(ind, puts, width, color = 'b', yerr=puts_std)
#rects2 = ax.bar(ind + width, gets, width, color = 'g', yerr=gets_std)
rects1 = ax.bar(ind, puts, width, yerr=np.vstack([puts_p10, puts_p90]))
rects2 = ax.bar(ind + width, gets, width, yerr=np.vstack([gets_p10, gets_p90]))

#rects1 = ax2.bar(ind, puts, width, color = 'b', yerr=puts_std)
#rects2 = ax2.bar(ind + width, gets, width, color = 'g', yerr=gets_std)
rects1 = ax2.bar(ind, puts, width, yerr=np.vstack([puts_p10, puts_p90]))
rects2 = ax2.bar(ind + width, gets, width, yerr=np.vstack([gets_p10, gets_p90]))
rects3 = ax2.bar(ind, delta_puts, width, yerr=np.vstack([cputs_p10, cputs_p90]), bottom=puts, color='lightgray')
rects4 = ax2.bar(ind + width, delta_gets, width, yerr=np.vstack([cgets_p10, cgets_p90]), bottom=gets, color='lightgray')
# add some text for labels, title and axes ticks
ax2.set_ylim(0,2000)
ax.set_ylim(10000,40000)
#ax.set_ylim(40000,140000)

# hide the spines between ax and ax2
ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)

ax.set_ylabel('Latency (us)')
ax.set_title('Unloaded latency for 1KB requests')
ax.set_xticks(ind + width / 2)
#ax.set_xticklabels(('S3', 'Redis', 'Crail-ReFlex'))
ax.set_xticklabels(('S3', 'Redis', 'Crail-ReFlex'))

ax.legend((rects1[0], rects2[0]), ('PUT', 'GET'))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.02*height,
                '%d' % int(height),
                ha='center', va='bottom')
        ax2.text(rect.get_x() + rect.get_width()/2., 1.02*height,
                '%d' % int(height),
                ha='center', va='bottom')

plt.rcParams.update({'font.size': 18})
autolabel(rects1)
autolabel(rects2)
height = put_crail
ax2.text(rects3[2].get_x() + rects3[2].get_width()/2., 1.12*height,
                '%d' % int(height),
                ha='center', va='bottom')
height = get_crail
ax2.text(rects4[2].get_x() + rects4[2].get_width()/2., 1.12*height,
                '%d' % int(height),
                ha='center', va='bottom')

fig.savefig("latency1KB.pdf")
plt.show()
