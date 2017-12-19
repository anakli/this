#!/bin/bash -ex


./fetch-redis-runlogs.py $1
./parse-runlogs.py $1 > timing_data
gnuplot timingbase.gnu
cp timing_data graphs/${1}.txt
cp graph.svg graphs/${1}.svg
