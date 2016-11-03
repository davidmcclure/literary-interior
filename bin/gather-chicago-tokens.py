#!/usr/bin/env python


from lint.singletons import config
from lint.models import TokenBin


if __name__ == '__main__':

    result_dir = config['results']['tokens']['chicago']

    TokenBin.gather_results('chicago', result_dir)
