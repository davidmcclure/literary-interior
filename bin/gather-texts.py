#!/usr/bin/env python


from lint.singletons import config
from lint.models import Text


if __name__ == '__main__':
    Text.gather(config['results']['texts'])
