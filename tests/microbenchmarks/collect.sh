#!/bin/sh

#zip decode-scanner.zip \
#    lambda.py DecoderAutomataCmd-static

rm *.zip

zip -9r latencyS3_microbenchmark.zip lambda.py __init__.py
