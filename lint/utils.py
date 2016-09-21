

import psutil
import os
import decimal
import re
import scandir

from collections import Counter
from contextlib import contextmanager
from itertools import islice, chain

from textblob import TextBlob

from lint.singletons import tokens as whitelist


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


def scan_paths(root, pattern):

    """
    Walk a directory and yield file paths that match a pattern.

    Args:
        root (str)
        pattern (str)

    Yields: str
    """

    pattern = re.compile(pattern)

    for root, dirs, files in scandir.walk(root, followlinks=True):
        for name in files:

            # Match the extension.
            if pattern.search(name):
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


def offset_counts(text, resolution):

    """
    Given a string of text, map (token, POS, offset) -> count.

    Args:
        text (str)
        resolution (int)

    Returns: Counter
    """

    # TODO: Use OpenNLP, for consistency with Hathi?

    blob = TextBlob(text)

    tags = blob.tags

    letters = re.compile('^[a-z]+$')

    counts = Counter()

    for i, (token, pos) in enumerate(tags):

        token = token.lower()

        # Ignore irregular tokens.
        if not letters.match(token):
            continue

        # Apply token whitelist.
        if token not in whitelist:
            continue

        # 0-1 offset ratio.
        ratio = i / len(tags)

        # Round offset to 0-N integer.
        offset = round(ratio * resolution)

        counts[token, pos, offset] += 1

    return counts
