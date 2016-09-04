#!/usr/bin/env python


from lint.singletons import config
from lint.models import Offset


if __name__ == '__main__':
    Offset.gather_results(config['offsets']['htrc'])
