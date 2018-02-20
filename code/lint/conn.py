

import boto3

from pyspark import SparkContext
from pyspark.sql import SparkSession

from .utils import LazySpacy


sc = SparkContext.getOrCreate()

spark = SparkSession.builder.getOrCreate()

nlp = LazySpacy()

s3 = boto3.resource('s3')
