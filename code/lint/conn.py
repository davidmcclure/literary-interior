

import boto3

from pyspark import SparkContext
from pyspark.sql import SparkSession


sc = SparkContext()

spark = SparkSession(sc).builder.getOrCreate()

s3 = boto3.resource('s3')
