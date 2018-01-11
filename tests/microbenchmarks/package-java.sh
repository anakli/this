#!/bin/sh

#zip decode-scanner.zip \
#    lambda.py DecoderAutomataCmd-static

rm *.zip

#zip -9r latency_microbenchmark.zip lambda.py redis __init__.py
zip -9r java.zip lambda_java.py log4j.properties reflex-client-1.0.jar reflex-client-1.0-jar-with-dependencies.jar reflex-client-1.0-tests.jar  __init__.py
