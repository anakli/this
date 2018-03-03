#!/bin/sh

#rm mxnet.zip
#zip -r mxnet.zip lambda_function.py certifi graphviz chardet numpy PIL requests urllib3 idna olefile mxnet
#zip -r .

rm *.zip
zip -r mxnet.zip *
aws lambda update-function-code --function-name mxnet-lambda-redis --zip-file fileb:///home/ubuntu/this/lambdas/mxnet-serverless/lambda-launched-redis/mxnet.zip
