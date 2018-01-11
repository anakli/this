#!/bin/sh

#zip decode-scanner.zip \
#    lambda.py DecoderAutomataCmd-static

rm *.zip

#zip -9r latency_microbenchmark.zip lambda.py redis __init__.py
cp lambda_throughput_s3.py lambda.py
zip -9r throughputs3_microbenchmark.zip lambda.py ifcfg __init__.py
