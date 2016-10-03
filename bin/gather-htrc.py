#!/usr/bin/env python


from lint.singletons import config
from lint.models import Word


if __name__ == '__main__':
    Word.gather_results('htrc', config['results']['htrc'])
