#!/bin/sh

#rm mxnet.zip
#zip -r mxnet.zip lambda_function.py certifi graphviz chardet numpy PIL requests urllib3 idna olefile mxnet
#zip -r .

rm *.zip
zip -9r mxnet-pocket.zip *
aws lambda update-function-code --function-name mxnet-lambda-pocket --zip-file fileb:///home/ubuntu/this/lambdas/mxnet-serverless/lambda-pocket/mxnet-pocket.zip
