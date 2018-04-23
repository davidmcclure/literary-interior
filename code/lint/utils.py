

import re
import logging
import csv
import math

from pyspark import SparkContext
from pyspark.sql import SparkSession

from functools import wraps

from . import fs


def get_spark():
    """Get spark connections.
    """
    sc = SparkContext.getOrCreate()
    spark = SparkSession(sc).builder.getOrCreate()

    return sc, spark


def try_or_none(func):
    """Call function in a try block. On error, return None.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        log = logging.getLogger('lint')

        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
            return None

    return wrapper


class cached_class_property:

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        """Call function and cache result as class property.
        https://github.com/pydanny/cached-property
        """
        value = self.func(cls)
        setattr(cls, self.func.__name__, value)
        return value


def read_csv(path):
    """Generate row dicts from CSV.
    """
    lines = fs.read(path).read().decode().splitlines()
    yield from csv.DictReader(lines)


def clean_text(text):
    """Clean a raw text string.
    """
    return re.sub('\s+', ' ', text.strip())


def zip_offset(seq):
    """Yield (item, 0-1 offset).
    """
    size = len(seq)
    for i, item in enumerate(seq):
        offset = i / (size - 1) if (size - 1) else 0
        yield item, offset


def zip_bin(seq, bin_count):
    """Yield (item, bin)
    """
    for item, offset in zip_offset(seq):
        bin = math.floor(offset * bin_count) if offset < 1 else bin_count - 1
        yield item, bin


def read_vocab_file(path):
    """One word per line.
    """
    with open(path) as fh:
        return fh.read().splitlines()
