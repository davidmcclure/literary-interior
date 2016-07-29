

import psutil
import os

from itertools import islice, chain
from contextlib import contextmanager


def grouper(iterable, size):

    """
    Yield "groups" from an iterable.

    Args:
        iterable (iter): The iterable.
        size (int): The number of elements in each group.

    Yields:
        The next group.
    """

    source = iter(iterable)

    while True:
        group = islice(source, size)
        yield chain([next(group)], group)


def flatten_dict(d):

    """
    Flatten a dict into a list of tuples.

    Args:
        nested (dict)

    Returns: tuple
    """

    for k, v in d.items():

        if isinstance(v, dict):
            for item in flatten_dict(v):
                yield (k,) + item

        else:
            yield (k, v)


@contextmanager
def open_makedirs(fpath, *args, **kwargs):

    """
    Create the directory for a file, open it.
    """

    path = os.path.dirname(fpath)

    os.makedirs(path, exist_ok=True)

    with open(fpath, *args, **kwargs) as fh:
        yield fh


def mem_pct():

    """
    Get the percentage of available memory used by the process.

    Returns: float
    """

    mem = psutil.virtual_memory()

    return mem.percent
