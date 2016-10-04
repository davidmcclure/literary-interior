#!/usr/bin/env python


from lint.singletons import config
from lint.models import Char


if __name__ == '__main__':

    result_dir = config['results']['chars']['chicago']

    Char.gather_results('chicago', result_dir)
