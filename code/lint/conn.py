

import boto3

from pyspark import SparkContext
from pyspark.sql import SparkSession


sc = SparkContext.getOrCreate()

spark = SparkSession.builder.getOrCreate()

s3 = boto3.resource('s3')
