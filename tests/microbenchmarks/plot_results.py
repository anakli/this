import numpy as np
import matplotlib.pyplot as plt

N = 3

redis_put_times = [703.0963897705078, 640.869140625, 628.9482116699219, 702.1427154541016, 662.0883941650391, 582.9334259033203, 653.9821624755859, 674.0093231201172, 604.1526794433594, 627.0408630371094, 602.9605865478516, 586.9865417480469, 575.0656127929688, 582.2181701660156, 635.1470947265625, 604.8679351806641, 653.9821624755859, 610.1131439208984, 711.9178771972656, 619.8883056640625, 728.1303405761719, 802.0401000976562, 630.8555603027344, 1230.001449584961, 617.98095703125, 576.9729614257812, 637.054443359375, 729.0840148925781, 663.9957427978516, 629.9018859863281, 681.8771362304688, 663.0420684814453, 715.9709930419922, 661.8499755859375, 641.1075592041016, 671.8635559082031, 681.8771362304688, 602.0069122314453, 683.0692291259766, 622.9877471923828, 643.0149078369141, 679.01611328125, 654.9358367919922, 622.9877471923828, 600.0995635986328, 599.1458892822266, 571.0124969482422, 663.0420684814453, 671.8635559082031, 645.8759307861328, 617.98095703125, 576.019287109375, 622.0340728759766, 1273.8704681396484, 669.0025329589844, 594.1390991210938, 627.9945373535156, 590.0859832763672, 695.9438323974609, 637.054443359375, 934.1239929199219, 623.9414215087891, 650.1674652099609, 581.0260772705078, 608.9210510253906, 560.9989166259766, 612.0204925537109, 627.0408630371094, 677.1087646484375, 599.8611450195312, 667.0951843261719, 591.9933319091797, 688.0760192871094, 649.2137908935547, 666.1415100097656, 615.1199340820312, 589.1323089599609, 573.8735198974609, 705.0037384033203, 591.9933319091797, 643.9685821533203, 622.0340728759766, 666.8567657470703, 663.0420684814453, 688.0760192871094, 622.0340728759766, 665.9030914306641, 600.8148193359375, 658.9889526367188, 711.9178771972656, 602.0069122314453, 670.1946258544922, 706.9110870361328, 624.8950958251953, 632.0476531982422, 582.9334259033203, 607.9673767089844, 575.0656127929688, 570.7740783691406]

redis_get_times = [635.8623504638672, 590.0859832763672, 622.0340728759766, 566.0057067871094, 599.8611450195312, 578.1650543212891, 653.9821624755859, 607.9673767089844, 626.0871887207031, 571.0124969482422, 586.0328674316406, 644.2070007324219, 803.9474487304688, 581.0260772705078, 736.9518280029297, 617.98095703125, 606.0600280761719, 626.8024444580078, 710.9642028808594, 605.8216094970703, 633.0013275146484, 607.0137023925781, 618.9346313476562, 649.9290466308594, 653.9821624755859, 574.1119384765625, 710.0105285644531, 586.9865417480469, 642.0612335205078, 656.8431854248047, 627.9945373535156, 560.0452423095703, 715.9709930419922, 570.0588226318359, 672.8172302246094, 623.2261657714844, 720.0241088867188, 625.1335144042969, 681.1618804931641, 577.9266357421875, 669.9562072753906, 611.7820739746094, 644.9222564697266, 588.8938903808594, 589.1323089599609, 627.0408630371094, 634.9086761474609, 610.1131439208984, 634.9086761474609, 661.1347198486328, 586.0328674316406, 567.1977996826172, 682.1155548095703, 563.8599395751953, 730.0376892089844, 615.8351898193359, 679.9697875976562, 624.8950958251953, 613.9278411865234, 571.0124969482422, 720.0241088867188, 576.9729614257812, 615.1199340820312, 588.8938903808594, 731.9450378417969, 539.0644073486328, 690.9370422363281, 573.1582641601562, 594.8543548583984, 626.0871887207031, 616.0736083984375, 550.9853363037109, 642.0612335205078, 566.0057067871094, 665.9030914306641, 591.0396575927734, 726.9382476806641, 586.0328674316406, 744.1043853759766, 625.1335144042969, 668.0488586425781, 587.9402160644531, 648.9753723144531, 633.0013275146484, 627.9945373535156, 575.0656127929688, 635.8623504638672, 599.8611450195312, 719.0704345703125, 596.0464477539062, 633.9550018310547, 549.7932434082031, 714.0636444091797, 579.1187286376953, 643.9685821533203, 571.9661712646484, 718.8320159912109, 563.1446838378906, 696.1822509765625]

put_redis = np.mean(redis_put_times) 
get_redis = np.mean(redis_get_times) 

s3_put_times = [41.79096221923828, 87.56613731384277, 50.62103271484375, 51.60808563232422, 1214.015007019043, 53.49087715148926, 55.03201484680176, 109.48705673217773, 96.98987007141113, 80.62601089477539, 57.91807174682617, 167.572021484375, 38.70201110839844, 38.8028621673584, 55.87887763977051, 52.23393440246582, 84.52820777893066, 96.47512435913086, 90.80791473388672, 41.380882263183594, 53.09891700744629, 63.02189826965332, 38.50603103637695, 40.60697555541992, 49.72195625305176, 87.76593208312988, 278.10215950012207, 88.14215660095215, 41.97382926940918, 65.5829906463623, 37.832021713256836, 46.96393013000488, 47.87111282348633, 1236.393928527832, 43.44606399536133, 66.01977348327637, 50.26602745056152, 54.34703826904297, 32.60087966918945, 42.218923568725586, 68.1309700012207, 58.834075927734375, 75.33001899719238, 45.610904693603516, 56.61511421203613, 47.601938247680664, 47.90806770324707, 68.99404525756836, 58.44402313232422, 33.8129997253418, 34.14201736450195, 66.34998321533203, 50.22287368774414, 48.22111129760742, 43.328046798706055, 48.542022705078125, 84.43093299865723, 41.21589660644531, 59.01312828063965, 58.91609191894531, 63.83681297302246, 48.77901077270508, 35.75301170349121, 69.60391998291016, 51.75304412841797, 85.99495887756348, 76.18904113769531, 57.90901184082031, 61.663150787353516, 44.28601264953613, 67.24214553833008, 44.08097267150879, 68.57180595397949, 71.5949535369873, 74.49507713317871, 65.72604179382324, 32.62495994567871, 31.143903732299805, 34.67202186584473, 36.3619327545166, 103.60503196716309, 78.46212387084961, 60.79602241516113, 57.98792839050293, 32.7000617980957, 58.61496925354004, 35.262107849121094, 45.266151428222656, 106.89377784729004, 31.406164169311523, 48.731088638305664, 53.4360408782959, 34.271955490112305, 34.9578857421875, 37.268877029418945, 30.970096588134766, 35.05301475524902, 56.635141372680664, 46.62299156188965] * 1000
s3_put_times = [i * 1000 for i in s3_put_times]

s3_get_times = [129.43506240844727, 76.42102241516113, 79.2078971862793, 176.13887786865234, 129.03785705566406, 77.20685005187988, 79.03599739074707, 86.13300323486328, 75.38199424743652, 76.06196403503418, 126.31392478942871, 79.02312278747559, 91.64786338806152, 76.45702362060547, 129.2128562927246, 78.88317108154297, 76.12395286560059, 76.72715187072754, 79.10680770874023, 80.39402961730957, 176.23209953308105, 147.1080780029297, 192.3229694366455, 75.98304748535156, 131.270170211792, 80.70111274719238, 83.19783210754395, 80.78694343566895, 87.08310127258301, 80.74402809143066, 146.9728946685791, 80.31916618347168, 78.15098762512207, 79.36906814575195, 76.92599296569824, 80.88207244873047, 80.91998100280762, 75.57010650634766, 153.58901023864746, 76.22289657592773, 76.49421691894531, 76.52997970581055, 127.04586982727051, 78.04512977600098, 126.55282020568848, 126.76405906677246, 77.34012603759766, 76.60698890686035, 530.3521156311035, 125.21195411682129, 178.5728931427002, 125.1230239868164, 126.88612937927246, 79.24485206604004, 76.36594772338867, 82.82995223999023, 76.37214660644531, 82.84401893615723, 126.43814086914062, 132.5669288635254, 85.2961540222168, 129.9288272857666, 85.96992492675781, 76.3390064239502, 75.79302787780762, 96.01902961730957, 128.30805778503418, 81.30598068237305, 79.58412170410156, 77.95500755310059, 78.80592346191406, 79.9410343170166, 87.2189998626709, 76.33399963378906, 87.55302429199219, 76.81608200073242, 80.32894134521484, 127.69293785095215, 92.2091007232666, 80.48605918884277, 127.77209281921387, 79.80990409851074, 77.6221752166748, 81.21895790100098, 132.25507736206055, 285.006046295166, 84.85794067382812, 78.10211181640625, 126.27601623535156, 76.96914672851562, 87.05401420593262, 126.29485130310059, 129.58502769470215, 76.02596282958984, 83.0080509185791, 75.72197914123535, 77.0869255065918, 125.72479248046875, 676.980972290039] 
s3_get_times = [i * 1000 for i in s3_get_times]


put_s3 = np.mean(s3_put_times) 
get_s3 = np.mean(s3_get_times) 

crail_put_times = [160, 250, 150] # averaged from 10K iterations
crail_get_times = [135, 125, 135]

put_crail = np.mean(crail_put_times)
get_crail = np.mean(crail_get_times)

puts = (put_s3, put_redis, put_crail)
gets = (get_s3, get_redis, get_crail)

puts_std = (np.std(s3_put_times), np.std(redis_put_times), np.std(crail_put_times))
gets_std = (np.std(s3_get_times), np.std(redis_get_times), np.std(crail_get_times))

puts_p10 = [np.mean(i) - np.percentile(i, 10) for i in [s3_put_times, redis_put_times, crail_put_times]]
gets_p10 = [np.mean(i) - np.percentile(i, 10) for i in [s3_get_times, redis_get_times, crail_get_times]]

puts_p90 = [np.percentile(i, 90) - np.mean(i) for i in [s3_put_times, redis_put_times, crail_put_times]]
gets_p90 = [np.percentile(i, 90) - np.mean(i) for i in [s3_get_times, redis_get_times, crail_get_times]]

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
