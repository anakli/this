#!/bin/bash -ex

~/crail/crail-deployment/crail-1.0/bin/crail fs -ls /video-lambda-logs | grep "netstats" | awk '{ print $8 }' | sed -e 's/\/video-lambda-logs\/netstats-//' > ~/this/logs/crail-runlog-reqids.txt
./fetch-crail-runlogs.py $1
./parse-runlogs.py $1 > timing_data
gnuplot timingbase.gnu
cp timing_data graphs/${1}.txt
cp graph.svg graphs/${1}.svg
