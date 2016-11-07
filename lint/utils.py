

import psutil
import os
import decimal
import re
import scandir
import math

from collections import Counter
from contextlib import contextmanager
from itertools import islice, chain

from textblob import TextBlob


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


def flatten_dict(d, root=True):

    """
    Flatten a dict into a list of tuples.

    Args:
        nested (dict)

    Yields: ((key1, key2, ...), val)
    """

    for k, v in d.items():

        if isinstance(v, dict):
            for item in flatten_dict(v, False):

                # At root level, break away the key path from the value.
                if root:
                    yield ((k,) + item[:-1], item[-1])

                # Otherwise build up the key chain.
                else:
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


def round_to_decade(year):

    """
    Round a year to the nearest decade.

    Args:
        year (int)

    Returns: int
    """

    decades = decimal.Decimal(year/10)

    rounded = decades.quantize(
        decimal.Decimal(1),
        rounding=decimal.ROUND_HALF_UP,
    )

    return int(rounded) * 10


def scan_paths(root, pattern=None):

    """
    Walk a directory and yield file paths that match a pattern.

    Args:
        root (str)
        pattern (str)

    Yields: str
    """

    for root, dirs, files in scandir.walk(root, followlinks=True):
        for name in files:

            # Match the extension.
            if not pattern or re.search(pattern, name):
                yield os.path.join(root, name)


def get_text(tree, selector):

    """
    Extract text from an element. Return None if the element is missing or the
    value is empty.

    Args:
        tree (BeautifulSoup)
        selector (str)

    Returns: str|None
    """

    tag = tree.select_one(selector)

    if tag:
        return ' '.join(tag.stripped_strings) or None

    else:
        return None


def make_offset(i, n, bins):

    """
    Given the index of the current token, the total number of tokens, and a bin
    count, round to a 1-N integer.

    Args:
        i (int)
        n (int)
        bins (int)

    Returns: int
    """

    return math.floor((i/n) * bins)


def clean_text(text):

    """
    Clean a raw text string.

    Args:
        text (str)

    Returns: str
    """

    return re.sub('\s{2,}', ' ', text.strip())


def clean_token(token):

    """
    Clean an individual token.

    - Downcase.
    - Strip leading / trailing non-[a-z] characters.

    Args:
        token (str)

    Returns: str
    """

    return re.sub('^[^a-z]*|[^a-z]*$', '', token.lower())


def pos_tag(text: str):

    """
    ASCII-encode and POS-tag a text.
    """

    # UTF8 -> ASCII.
    blob = TextBlob(text.encode('ascii', 'ignore').decode())

    return blob.tags
