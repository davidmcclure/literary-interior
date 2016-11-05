#!/usr/bin/env python


from lint.singletons import config
from lint.models import Bucket


if __name__ == '__main__':

    result_dir = config['results']['bins']['gail']

    Bucket.gather_results('gail', result_dir)
