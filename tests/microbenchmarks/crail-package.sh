#!/bin/sh

#zip decode-scanner.zip \
#    lambda.py DecoderAutomataCmd-static

rm *.zip

#zip -9r latency_microbenchmark.zip lambda.py redis __init__.py
#zip -9r java.zip lambda_java.py log4j.properties crail-reflex-1.0.jar reflex-client-1.0-jar-with-dependencies.jar crail-client-1.0.jar bin conf __init__.py
#zip -9r java.zip lambda_java.py crail-reflex-1.0.jar reflex-client-1.0-jar-with-dependencies.jar crail-client-1.0.jar bin conf jars __init__.py
zip -9r java.zip lambda_java.py bin conf jars __init__.py
