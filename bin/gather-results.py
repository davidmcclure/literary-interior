#!/usr/bin/env python


from lint.singletons import config
from lint.models import Offset


def gather_results():

    """
    Insert the offsets into the database.
    """

    Offset.gather_results(config['offsets']['htrc'])


if __name__ == '__main__':
    gather_results()
