#!/usr/bin/env python


from lint.singletons import config
from lint.models import Char


if __name__ == '__main__':

    result_dir = config['results']['gail']['chars']

    Char.gather_results('gail', result_dir)
