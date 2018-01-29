#!/bin/bash -ex

#~/crail/crail-deployment/crail-1.0/bin/crail fs -ls /runlogs | grep -v "lambda" | grep -v "Found" | awk '{ print $8 }' | sed -e 's/\/runlogs\///' > ~/this/logs/crail-runlog-reqids.txt
#~/crail/crail-deployment/crail-1.0/bin/crail fs -ls /runlogs | grep "runlogs" | awk '{ print $8 }' | sed -e 's/\/runlogs\///' > ~/this/logs/crail-runlog-reqids.txt
ls /home/ubuntu/$2/.gg/blobs/runlogs > ~/this/logs/crail-runlog-reqids.txt
./fetch-crail-gg-runlogs.py $1
./parse-runlogs.py $1 > timing_data
gnuplot timingbase_gg.gnu
cp timing_data graphs/${1}.txt
cp graph.svg graphs/${1}.svg
