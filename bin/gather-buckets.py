#!/usr/bin/env python


from lint.singletons import config
from lint.models import Bucket


if __name__ == '__main__':
    Bucket.gather(config['results']['buckets'])
