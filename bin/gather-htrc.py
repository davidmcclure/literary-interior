#!/usr/bin/env python


from lint.singletons import config, session
from lint.models import Offset
from lint.count_cache import CountCache


if __name__ == '__main__':
    Offset.gather_results('htrc', config['results']['htrc'])
