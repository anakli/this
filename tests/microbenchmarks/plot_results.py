import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style

plt.style.use('default')
plt.rcParams.update({'font.size': 24})
plt.rcParams['errorbar.capsize'] = 2

N = 3

#single node, i3.8xlarge, replication factor 1
aerospike_DRAM_put_times = [151,169,171,169, 184, 166]
aerospike_DRAM_get_times = [141,162,155,157, 166, 162]

#single node, i3.8xlarge, replication factor 1
#aerospike_NVMe_put_times = [179,188,181,169, 181]
#aerospike_NVMe_get_times = [172,175,173,161, 168]
aerospike_NVMe_put_times = [225, 219, 223, 203,213]
aerospike_NVMe_get_times = [206, 201, 210, 186,204] 

#elasticache
redis_put_times = [190, 250, 240, 270, 260, 260] 
redis_get_times = [190, 200, 240, 250, 260, 260] 

# 3shard 0 replica c4.8xlarge
rediscluster_put_times = [546.9322204589844, 202.178955078125, 245.80955505371094, 293.0164337158203, 303.03001403808594, 246.0479736328125, 288.0096435546875, 245.09429931640625, 212.9077911376953, 252.9621124267578, 257.0152282714844, 235.08071899414062, 204.0863037109375, 337.83912658691406, 239.1338348388672, 231.02760314941406, 187.87384033203125, 289.9169921875, 221.9676971435547, 200.9868621826172, 205.99365234375, 287.05596923828125, 299.9305725097656, 218.1529998779297, 235.08071899414062, 204.0863037109375, 251.0547637939453, 218.1529998779297, 250.10108947753906, 262.97569274902344, 269.88983154296875, 222.20611572265625, 267.98248291015625, 205.99365234375, 273.9429473876953, 211.95411682128906, 285.86387634277344, 262.97569274902344, 224.11346435546875, 292.06275939941406, 251.0547637939453, 241.99485778808594, 209.0930938720703, 290.15541076660156, 309.94415283203125, 231.02760314941406, 214.09988403320312, 266.07513427734375, 240.80276489257812, 284.9102020263672, 236.98806762695312, 293.0164337158203, 219.10667419433594, 271.08192443847656, 290.87066650390625, 216.00723266601562, 285.14862060546875, 287.05596923828125, 199.0795135498047, 267.02880859375, 284.9102020263672, 222.92137145996094, 296.1158752441406, 238.18016052246094, 241.0411834716797, 192.16537475585938, 300.8842468261719, 266.07513427734375, 237.94174194335938, 189.06593322753906, 283.0028533935547, 293.97010803222656, 281.0955047607422, 186.920166015625, 236.98806762695312, 294.9237823486328, 284.9102020263672, 188.8275146484375, 186.920166015625, 185.0128173828125, 313.04359436035156, 220.0603485107422, 292.06275939941406, 209.808349609375, 308.03680419921875, 253.91578674316406, 211.0004425048828, 190.0196075439453, 287.05596923828125, 297.0695495605469, 236.98806762695312, 189.06593322753906, 314.95094299316406, 280.8570861816406, 214.09988403320312, 205.99365234375, 249.1474151611328, 308.03680419921875, 235.08071899414062, 264.88304138183594, 283.95652770996094, 293.97010803222656, 216.96090698242188, 246.0479736328125, 216.00723266601562, 252.00843811035156, 185.96649169921875, 256.0615539550781, 230.0739288330078, 235.08071899414062, 293.0164337158203, 212.9077911376953, 221.01402282714844, 283.0028533935547, 287.05596923828125, 255.10787963867188, 182.15179443359375, 277.9960632324219, 178.81393432617188, 227.92816162109375, 267.98248291015625, 186.920166015625, 263.9293670654297, 227.21290588378906, 283.0028533935547, 188.1122589111328, 256.0615539550781, 255.82313537597656, 245.09429931640625, 193.11904907226562, 283.0028533935547, 267.98248291015625, 236.98806762695312, 200.9868621826172, 269.88983154296875, 227.92816162109375, 217.19932556152344, 208.13941955566406, 221.9676971435547, 247.00164794921875, 231.02760314941406, 218.1529998779297, 236.03439331054688, 293.97010803222656, 272.0355987548828, 279.1881561279297, 206.94732666015625, 272.98927307128906, 278.9497375488281, 308.03680419921875, 293.97010803222656, 230.0739288330078, 184.05914306640625, 308.03680419921875, 295.87745666503906, 241.99485778808594, 184.05914306640625, 234.12704467773438, 181.9133758544922, 203.84788513183594, 292.06275939941406, 272.0355987548828, 288.0096435546875, 218.86825561523438, 277.0423889160156, 306.12945556640625, 264.88304138183594] 
rediscluster_get_times = [232.93495178222656, 238.18016052246094, 203.13262939453125, 266.07513427734375, 276.0887145996094, 284.1949462890625, 211.95411682128906, 230.0739288330078, 288.0096435546875, 204.8015594482422, 231.02760314941406, 237.94174194335938, 304.93736267089844, 205.99365234375, 288.96331787109375, 229.83551025390625, 233.8886260986328, 187.87384033203125, 258.9225769042969, 182.86705017089844, 178.0986785888672, 245.09429931640625, 232.93495178222656, 282.04917907714844, 204.0863037109375, 239.1338348388672, 258.2073211669922, 278.9497375488281, 225.7823944091797, 277.9960632324219, 229.12025451660156, 219.10667419433594, 195.02639770507812, 231.02760314941406, 229.12025451660156, 206.94732666015625, 178.81393432617188, 287.05596923828125, 280.14183044433594, 195.02639770507812, 233.17337036132812, 202.178955078125, 225.067138671875, 180.0060272216797, 233.8886260986328, 285.86387634277344, 277.9960632324219, 208.13941955566406, 247.00164794921875, 232.93495178222656, 271.08192443847656, 247.955322265625, 231.9812774658203, 181.9133758544922, 240.80276489257812, 231.9812774658203, 183.8207244873047, 205.99365234375, 239.1338348388672, 183.10546875, 220.0603485107422, 276.0887145996094, 209.0930938720703, 236.98806762695312, 283.0028533935547, 248.90899658203125, 179.05235290527344, 237.94174194335938, 234.84230041503906, 225.067138671875, 175.95291137695312, 260.8299255371094, 281.0955047607422, 232.93495178222656, 192.88063049316406, 231.9812774658203, 231.02760314941406, 231.9812774658203, 174.99923706054688, 174.99923706054688, 216.96090698242188, 280.8570861816406, 234.84230041503906, 219.10667419433594, 180.95970153808594, 277.9960632324219, 236.03439331054688, 220.0603485107422, 200.9868621826172, 281.0955047607422, 242.9485321044922, 221.01402282714844, 199.79476928710938, 252.9621124267578, 275.1350402832031, 234.12704467773438, 201.94053649902344, 253.91578674316406, 278.9497375488281, 293.0164337158203, 240.08750915527344, 208.13941955566406, 277.9960632324219, 205.03997802734375, 264.88304138183594, 211.0004425048828, 223.1597900390625, 200.03318786621094, 238.89541625976562, 220.0603485107422, 201.94053649902344, 281.0955047607422, 217.19932556152344, 236.98806762695312, 231.02760314941406, 241.0411834716797, 235.08071899414062, 202.178955078125, 231.02760314941406, 180.0060272216797, 225.067138671875, 273.9429473876953, 181.9133758544922, 294.9237823486328, 207.9010009765625, 252.00843811035156, 185.96649169921875, 236.03439331054688, 283.0028533935547, 225.067138671875, 198.84109497070312, 252.00843811035156, 290.15541076660156, 210.04676818847656, 181.1981201171875, 278.9497375488281, 270.843505859375] ##TODO

put_redis = np.mean(redis_put_times) 
get_redis = np.mean(redis_get_times) 


# reuse connection
s3_put_times = [12.067079544067383, 26.093006134033203, 13.40794563293457, 12.431859970092773, 37.940025329589844, 14.700174331665039, 33.01811218261719, 41.6719913482666, 23.864030838012695, 38.65790367126465, 14.305830001831055, 23.44202995300293, 86.7011547088623, 11.925935745239258, 34.28816795349121, 13.671159744262695, 33.442020416259766, 39.827823638916016, 35.41302680969238, 15.94686508178711, 60.951948165893555, 12.349843978881836, 23.717880249023438, 12.788057327270508, 13.111114501953125, 17.69709587097168, 13.820886611938477, 140.97285270690918, 11.825084686279297, 28.890132904052734, 36.972999572753906, 12.691020965576172, 14.983177185058594, 58.598995208740234, 32.15193748474121, 13.931989669799805, 14.278888702392578, 57.704925537109375, 32.753944396972656, 12.614011764526367, 32.59015083312988, 14.497995376586914, 13.503074645996094, 50.7810115814209, 12.394905090332031, 76.81798934936523, 39.090871810913086, 16.277074813842773, 16.139984130859375, 14.047861099243164, 40.94099998474121, 16.5250301361084, 14.309883117675781, 15.999794006347656, 14.013051986694336, 13.313055038452148, 12.482881546020508, 14.369964599609375, 44.46291923522949, 15.41900634765625, 15.68913459777832, 18.702030181884766, 15.831947326660156, 24.362802505493164, 14.17994499206543, 16.74795150756836, 13.879776000976562, 14.997005462646484, 13.97705078125, 16.32404327392578, 25.730133056640625, 14.278888702392578, 41.40591621398926, 15.32292366027832, 15.24209976196289, 30.878067016601562, 46.52881622314453, 32.50312805175781, 13.847827911376953, 13.261079788208008, 36.93795204162598, 15.81716537475586, 34.88612174987793, 15.079975128173828, 14.056921005249023, 35.817861557006836, 11.91401481628418, 39.2909049987793, 34.158945083618164, 16.150951385498047, 14.715194702148438, 16.152143478393555, 14.439105987548828, 19.64712142944336, 46.462059020996094] * 1000


s3_put_times = [i * 1000 for i in s3_put_times]


s3_get_times = [12.73202896118164, 11.67607307434082, 13.145923614501953, 11.209964752197266, 14.107227325439453, 14.23501968383789, 10.837793350219727, 13.384103775024414, 12.944936752319336, 15.459060668945312, 11.758089065551758, 12.771844863891602, 12.898921966552734, 12.603998184204102, 9.307146072387695, 13.100147247314453, 11.671066284179688, 11.946916580200195, 14.938831329345703, 13.195037841796875, 11.26408576965332, 10.725975036621094, 11.380910873413086, 11.718988418579102, 11.291027069091797, 11.026144027709961, 11.557817459106445, 14.738082885742188, 11.896133422851562, 10.679006576538086, 11.986970901489258, 11.913061141967773, 10.174989700317383, 10.38217544555664, 11.175155639648438, 12.3291015625, 13.675928115844727, 12.231111526489258, 11.940956115722656, 11.207103729248047, 13.532161712646484, 12.896060943603516, 13.679981231689453, 11.126995086669922, 11.430978775024414, 12.230873107910156, 11.192083358764648, 11.924982070922852, 12.86005973815918, 15.659809112548828, 12.856006622314453, 13.281822204589844, 12.433052062988281, 9.638071060180664, 10.679960250854492, 11.701107025146484, 10.70404052734375, 11.027097702026367, 11.744022369384766, 10.690927505493164, 10.728836059570312, 9.881019592285156, 11.434078216552734, 19.029855728149414, 12.859821319580078, 11.897087097167969, 13.525962829589844, 12.073040008544922, 10.280132293701172, 10.553121566772461, 11.586904525756836, 10.730981826782227, 13.308048248291016, 13.51618766784668, 15.712976455688477, 10.987997055053711, 11.64698600769043, 12.214899063110352, 11.012077331542969, 10.030984878540039, 10.200977325439453, 10.32400131225586, 12.510061264038086, 13.037919998168945, 11.361837387084961, 11.021137237548828, 11.222124099731445, 12.002944946289062, 13.799905776977539, 12.824058532714844, 11.413097381591797, 10.262012481689453, 12.643814086914062, 12.187957763671875, 13.398885726928711]
s3_get_times = [i * 1000 for i in s3_get_times]


put_s3 = np.mean(s3_put_times) 
get_s3 = np.mean(s3_get_times) 

#crail_put_times = [160, 250, 150] # averaged from 10K iterations, one big file
#crail_put_times = [0] # FIXME: 
#crail_get_times = [135, 125, 135] 
#crail_get_times = [408, 476, 411, 421] # getKey

crail_put_times_noskipdir = [3808.9752197265625, 3741.9795989990234, 3700.9716033935547, 3596.067428588867, 7261.037826538086, 3593.2064056396484, 3529.071807861328, 3575.0865936279297, 3561.9735717773438, 7525.920867919922, 3525.0186920166016, 3603.9352416992188, 3471.851348876953, 11173.96354675293, 3561.9735717773438, 3514.0514373779297, 9469.985961914062, 3492.8321838378906, 3304.004669189453, 3417.0150756835938, 3412.961959838867, 3328.8002014160156, 3342.866897583008, 3307.819366455078, 3453.969955444336, 3433.9427947998047, 3252.9830932617188, 3415.1077270507812, 3301.1436462402344, 3448.009490966797, 3604.1736602783203, 3401.9947052001953, 3262.042999267578, 3409.147262573242, 3329.038619995117, 3479.9575805664062, 3446.1021423339844, 4048.1090545654297, 3214.120864868164, 3280.162811279297, 3365.039825439453, 3441.0953521728516, 3284.931182861328, 3371.000289916992, 3278.970718383789, 3417.0150756835938, 3288.9842987060547, 3460.8840942382812, 3239.870071411133, 3309.965133666992, 3346.9200134277344, 3182.8880310058594, 3325.939178466797, 3323.078155517578, 3360.0330352783203, 3160.9535217285156, 3158.092498779297, 3224.1344451904297, 3191.232681274414, 3180.0270080566406, 3314.971923828125, 3326.1775970458984, 3750.0858306884766, 3381.013870239258, 3280.8780670166016, 3208.8756561279297, 3263.9503479003906, 3233.194351196289, 3166.9139862060547, 3139.972686767578, 3195.047378540039, 3192.1863555908203, 3159.9998474121094, 3150.93994140625, 3190.9942626953125, 3263.9503479003906, 3262.9966735839844, 3236.055374145508, 3299.9515533447266, 3199.1004943847656, 3159.046173095703, 3146.8868255615234, 3227.9491424560547, 3315.9255981445312, 3459.2151641845703, 3215.0745391845703, 3163.0992889404297, 3139.972686767578, 3165.006637573242, 3157.8540802001953, 3168.1060791015625, 3141.164779663086, 3123.044967651367, 3330.9459686279297, 3447.0558166503906, 3283.0238342285156, 3237.9627227783203, 3145.933151245117, 3097.057342529297]


#skipdir, nodelay
crail_put_times = [706.9110870361328, 698.089599609375, 702.1427154541016, 777.0061492919922, 784.8739624023438, 782.012939453125, 786.0660552978516, 801.08642578125, 897.1691131591797, 2772.092819213867, 965.8336639404297, 983.9534759521484, 999.9275207519531, 840.9023284912109, 878.8108825683594, 799.8943328857422, 816.8220520019531, 679.01611328125, 679.9697875976562, 694.0364837646484, 728.1303405761719, 688.0760192871094, 640.1538848876953, 644.9222564697266, 633.0013275146484, 674.9629974365234, 658.9889526367188, 3108.0245971679688, 762.939453125, 679.9697875976562, 675.9166717529297, 687.8376007080078, 675.201416015625, 718.1167602539062, 818.0141448974609, 728.8455963134766, 661.1347198486328, 829.2198181152344, 713.8252258300781, 709.0568542480469, 747.9190826416016, 709.0568542480469, 694.9901580810547, 684.9765777587891, 705.0037384033203, 690.9370422363281, 688.0760192871094, 766.9925689697266, 708.8184356689453, 751.9721984863281, 732.8987121582031, 735.9981536865234, 802.0401000976562, 737.9055023193359, 684.9765777587891, 734.0908050537109, 715.0173187255859, 757.9326629638672, 725.9845733642578, 695.9438323974609, 715.9709930419922, 730.9913635253906, 702.1427154541016, 666.8567657470703, 687.1223449707031, 691.8907165527344, 746.9654083251953, 704.0500640869141, 715.9709930419922, 700.9506225585938, 699.0432739257812, 699.0432739257812, 720.977783203125, 1053.0948638916016, 737.1902465820312, 779.1519165039062, 828.9813995361328, 735.9981536865234, 712.1562957763672, 781.0592651367188, 689.0296936035156, 721.9314575195312, 800.1327514648438, 677.1087646484375, 717.8783416748047, 706.9110870361328, 724.0772247314453, 720.0241088867188, 736.9518280029297, 724.0772247314453, 727.8919219970703, 699.9969482421875, 720.977783203125, 717.1630859375, 739.8128509521484, 721.9314575195312, 702.1427154541016, 721.9314575195312, 712.1562957763672, 779.1519165039062, 724.0772247314453, 700.9506225585938, 723.1235504150391, 732.8987121582031, 713.1099700927734, 746.0117340087891, 745.0580596923828, 717.8783416748047, 697.1359252929688, 694.0364837646484, 725.0308990478516, 731.9450378417969, 721.9314575195312, 719.0704345703125, 705.0037384033203, 718.1167602539062, 712.8715515136719, 721.9314575195312, 706.9110870361328, 684.0229034423828, 711.9178771972656, 732.8987121582031, 729.0840148925781, 706.9110870361328, 741.9586181640625, 726.9382476806641]

#skipdir, nodelay
crail_get_times =[519.0372467041016, 514.0304565429688, 644.9222564697266, 509.02366638183594, 545.9785461425781, 527.8587341308594, 561.9525909423828, 503.0632019042969, 510.21575927734375, 472.78404235839844, 483.9897155761719, 528.0971527099609, 479.9365997314453, 568.8667297363281, 519.0372467041016, 517.1298980712891, 500.2021789550781, 504.9705505371094, 484.9433898925781, 555.9921264648438, 475.88348388671875, 479.9365997314453, 546.9322204589844, 567.9130554199219, 575.0656127929688, 512.1231079101562, 508.0699920654297, 534.0576171875, 511.16943359375, 521.8982696533203, 494.0032958984375, 475.88348388671875, 489.95018005371094, 472.06878662109375, 515.9378051757812, 485.8970642089844, 499.96376037597656, 479.9365997314453, 475.88348388671875, 478.0292510986328, 463.9625549316406, 487.8044128417969, 482.0823669433594, 535.0112915039062, 502.1095275878906, 498.05641174316406, 510.93101501464844, 540.0180816650391, 484.9433898925781, 497.8179931640625, 508.0699920654297, 520.9445953369141, 496.86431884765625, 551.9390106201172, 501.87110900878906, 539.0644073486328, 530.9581756591797, 505.9242248535156, 540.0180816650391, 534.0576171875, 501.87110900878906, 529.0508270263672, 541.9254302978516, 482.0823669433594, 473.97613525390625, 499.0100860595703, 480.89027404785156, 503.0632019042969, 482.0823669433594, 511.8846893310547, 535.0112915039062, 591.0396575927734, 527.8587341308594, 541.9254302978516, 530.9581756591797, 518.0835723876953, 561.9525909423828, 535.0112915039062, 519.9909210205078, 519.0372467041016, 529.0508270263672, 543.1175231933594, 498.05641174316406, 530.9581756591797, 494.0032958984375, 539.0644073486328, 480.1750183105469, 477.07557678222656, 494.0032958984375, 586.0328674316406, 469.207763671875, 462.7704620361328]


#crail_putkey_skipdir_times = [1960, 1749, 1716, 1977]
crail_putkey_skipdir_times = [350, 398, 323, 382, 381] #nodelay
crail_getkey_skipdir_times = [306, 289, 266, 293, 301, 319, 305] #334,337, 347, 319

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
