#!/usr/bin/env python


from lint.singletons import config
from lint.models import Token


if __name__ == '__main__':
    Token.gather_results('gail', config['results']['gail'])
