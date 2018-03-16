#!/bin/bash -ex

python gen-crail-lognames.py 63
python gen-crail-mxnet-lognames.py 63 312
./fetch-crail-mxnet-runlogs.py $1
stage1=$1
stage1+="_stage1"
./parse-runlogs.py $stage1 > timing_data
gnuplot timingbase.gnu
cp timing_data graphs/${stage1}.txt
cp graph.svg graphs/${stage1}.svg
python parse-netstats-withcpu.py $stage1
python plot-netstats-withcpu.py $stage1

stage2=$1
stage2+="_stage2"
./parse-runlogs.py $stage2 > timing_data
gnuplot timingbase.gnu
cp timing_data graphs/${stage2}.txt
cp graph.svg graphs/${stage2}.svg
python parse-netstats-withcpu.py $stage2
python plot-netstats-withcpu.py $stage2
