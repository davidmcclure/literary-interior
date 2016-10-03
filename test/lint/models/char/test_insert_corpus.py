

import pytest

from lint.count_cache import CountCache
from lint.models import Char


pytestmark = pytest.mark.usefixtures('db')


def test_insert_corpus():

    """
    Insert a row for each count tuple.
    """

    cache = CountCache()

    cache[1901, 'a', 1] = 1
    cache[1902, 'b', 2] = 2
    cache[1903, 'c', 3] = 3

    Char.insert_corpus('corpus', cache)

    assert Char.get('corpus', 1901, 'a', 1) == 1
    assert Char.get('corpus', 1902, 'b', 2) == 2
    assert Char.get('corpus', 1903, 'c', 3) == 3
