

import pytest

from lint.offset_cache import OffsetCache
from lint.models import Offset


pytestmark = pytest.mark.usefixtures('db')


def test_insert_corpus():

    """
    Insert a row for each year / token / offset / count.
    """

    cache = OffsetCache()

    cache[1901, 'token1', 'POS', 1] = 1
    cache[1902, 'token2', 'POS', 2] = 2
    cache[1903, 'token3', 'POS', 3] = 3

    Offset.insert_corpus('corpus', cache)

    assert Offset.get('corpus', 'token1', 1901, 1) == 1
    assert Offset.get('corpus', 'token2', 1902, 2) == 2
    assert Offset.get('corpus', 'token3', 1903, 3) == 3
