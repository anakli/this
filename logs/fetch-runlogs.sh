#!/bin/bash -ex

mkdir -p $1
aws s3 cp --recursive s3://video-lambda-logs/ $1/
