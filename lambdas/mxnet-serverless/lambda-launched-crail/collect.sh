#!/bin/sh

#rm mxnet.zip
#zip -r mxnet.zip lambda_function.py certifi graphviz chardet numpy PIL requests urllib3 idna olefile mxnet
#zip -r .

rm *.zip
zip -9r mxnet-crail.zip *
aws lambda update-function-code --function-name mxnet-lambda-crail --zip-file fileb:///home/ubuntu/this/lambdas/mxnet-serverless/lambda-launched-crail/mxnet-crail.zip
