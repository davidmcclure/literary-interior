

import pytest

from lint.count_cache import CountCache
from lint.models import Bucket


pytestmark = pytest.mark.usefixtures('db')


def test_insert_corpus():

    """
    Insert a row for each corpus / year / token / offset / count.
    """

    cache = CountCache()

    cache['corpus1', 1901, 'token1', 'POS1', 1] = 1
    cache['corpus2', 1902, 'token2', 'POS2', 2] = 2
    cache['corpus3', 1903, 'token3', 'POS3', 3] = 3

    Bucket.insert_corpus(cache)

    assert Bucket.get('corpus1', 1901, 'token1', 'POS1', 1) == 1
    assert Bucket.get('corpus2', 1902, 'token2', 'POS2', 2) == 2
    assert Bucket.get('corpus3', 1903, 'token3', 'POS3', 3) == 3
