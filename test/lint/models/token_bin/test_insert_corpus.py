

import pytest

from lint.count_cache import CountCache
from lint.models import TokenBin


pytestmark = pytest.mark.usefixtures('db')


def test_insert_corpus():

    """
    Insert a row for each year / token / offset / count.
    """

    cache = CountCache()

    cache[1901, 'token1', 'POS1', 1] = 1
    cache[1902, 'token2', 'POS2', 2] = 2
    cache[1903, 'token3', 'POS3', 3] = 3

    TokenBin.insert_corpus('corpus', cache)

    assert TokenBin.get('corpus', 1901, 'token1', 'POS1', 1) == 1
    assert TokenBin.get('corpus', 1902, 'token2', 'POS2', 2) == 2
    assert TokenBin.get('corpus', 1903, 'token3', 'POS3', 3) == 3
