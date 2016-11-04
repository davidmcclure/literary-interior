#!/usr/bin/env python


from lint.singletons import config
from lint.models import TokenBin


if __name__ == '__main__':

    result_dir = config['results']['bins']['gail']

    TokenBin.gather_results('gail', result_dir)
