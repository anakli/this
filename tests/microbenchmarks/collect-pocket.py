#!/bin/sh

#zip decode-scanner.zip \
#    lambda.py DecoderAutomataCmd-static

rm *.zip

cp lambda_throughput_pocket.py lambda_pocket.py
zip -9r throughput.zip lambda_pocket.py pocket.py lib*.so* ifcfg __init__.py
#cp lambda_latency_redis.py lambda.py
#zip -9r latency_microbenchmark.zip lambda.py redis __init__.py
#zip -9r throughput_microbenchmark.zip lambda.py redis ifcfg __init__.py

aws lambda update-function-code --function-name lambda-ubench-pocket --zip-file fileb:///home/ubuntu/this/tests/microbenchmarks/throughput.zip
