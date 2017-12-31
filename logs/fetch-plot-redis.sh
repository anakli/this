#!/bin/bash -ex

./plot-redis-breakdown.sh $1
./fetch-redis-netstats.py $1
./parse-netstats.py $1
./plot-netstats.py $1
