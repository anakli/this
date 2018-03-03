## Simple lambda microbenchmark for unloaded latency tests

import time
import sys
import redis
import boto3
import botocore
from multiprocessing.pool import ThreadPool
from threading import Semaphore, Lock
import progressbar
import json
from collections import OrderedDict
import argparse


#REQ_SIZE = (1048576*128)
#NUM_TRIALS = 20
REQ_SIZE = (1024 * 1024)
NUM_TRIALS = 100
NUM_LAMBDAS = 1
REDIS_HOSTADDR_PRIV = "elasti8xl.e4lofi.0001.usw2.cache.amazonaws.com" #TODO: set to correct url


client = boto3.client('lambda')

lambdaCount = 0
def invoke_lambdas(numLambdas, args):
  lambdaTotalCount = len(xrange(0, numLambdas))
  #bar = progressbar.ProgressBar(maxval=lambdaTotalCount,
  #      widgets=[progressbar.Bar('=', 'Lambdas   [', ']'), ' ',
  #               progressbar.Percentage()])
  #bar.start()
  global lambdaCount
  lambdaCount = 0
  MAX_PARALLEL_UPLOADS = numLambdas
  pool = ThreadPool(MAX_PARALLEL_UPLOADS)
  sema = Semaphore(MAX_PARALLEL_UPLOADS)
  countLock = Lock()
  results = []

  def invoke_lambda(lambda_id, args):
    sema.acquire()
    successCount = 1
    try:
      payload = OrderedDict()
      payload['num_trials'] = NUM_TRIALS
      payload['req_size'] = REQ_SIZE

      response = client.invoke(FunctionName=args.lambdaName,
                               InvocationType='Event',
                               Payload=str.encode(json.dumps(payload)))

      if response['StatusCode'] != 202:
        print('Error in invoking Lambda')
        successCount = 0

    finally:
      sema.release()
      global lambdaCount
      with countLock:
        lambdaCount += successCount
      #bar.update(lambdaCount)

  for lambda_id in xrange(0, numLambdas):
    result = pool.apply_async(invoke_lambda, args=(lambda_id, args))
    results.append(result)

  for result in results:
    result.get()

  for _ in xrange(MAX_PARALLEL_UPLOADS):
    sema.acquire()
  #bar.finish()

  return lambdaCount


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--function', '-f', type=str, required=True,
            dest='lambdaName',
            help='Which lambda function to use')
  return parser.parse_args()

def main(args):
  print('Argument list: {}'.format(args))
  invoke_lambdas(NUM_LAMBDAS, args)
  

if __name__ == '__main__':
  main(get_args())
