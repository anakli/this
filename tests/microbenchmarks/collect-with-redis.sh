#!/bin/sh

#zip decode-scanner.zip \
#    lambda.py DecoderAutomataCmd-static

rm *.zip

#zip -9r latency_microbenchmark.zip lambda.py redis __init__.py
zip -9r throughput_microbenchmark.zip lambda.py redis ifcfg __init__.py
