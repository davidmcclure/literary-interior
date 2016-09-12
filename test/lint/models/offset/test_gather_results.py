

import pytest

from lint.offset_cache import OffsetCache
from lint.models import Offset


pytestmark = pytest.mark.usefixtures('db')


def test_gather_results(htrc_results):

    c1 = OffsetCache()
    c1['token1'][1901][1] = 1
    c1['token2'][1902][1] = 2
    c1['token3'][1903][1] = 3

    c2 = OffsetCache()
    c2['token2'][1902][1] = 4
    c2['token3'][1903][1] = 5
    c2['token4'][1904][1] = 6

    c3 = OffsetCache()
    c3['token3'][1903][1] = 7
    c3['token4'][1904][1] = 8
    c3['token5'][1905][1] = 9

    htrc_results.add_cache(c1)
    htrc_results.add_cache(c2)
    htrc_results.add_cache(c3)

    Offset.gather_results('htrc', htrc_results.path)

    assert Offset.get('htrc', 'token1', 1901, 1) == 1
    assert Offset.get('htrc', 'token2', 1902, 1) == 2+4
    assert Offset.get('htrc', 'token3', 1903, 1) == 3+5+7
    assert Offset.get('htrc', 'token4', 1904, 1) == 6+8
    assert Offset.get('htrc', 'token5', 1905, 1) == 9
