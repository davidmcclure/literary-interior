#!/usr/bin/env python


from lint.singletons import config
from lint.models import Token


if __name__ == '__main__':

    result_dir = config['results']['chicago']['tokens']

    Token.gather_results('chicago', result_dir)
