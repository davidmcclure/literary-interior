

import pytest

from lint.offset_cache import OffsetCache
from lint.models import Offset


pytestmark = pytest.mark.usefixtures('db')


def test_gather_results(htrc_results):

    c1 = OffsetCache()
    c1[1901]['token1'][1] = 1
    c1[1902]['token2'][1] = 2
    c1[1903]['token3'][1] = 3

    c2 = OffsetCache()
    c2[1902]['token2'][1] = 4
    c2[1903]['token3'][1] = 5
    c2[1904]['token4'][1] = 6

    c3 = OffsetCache()
    c3[1903]['token3'][1] = 7
    c3[1904]['token4'][1] = 8
    c3[1905]['token5'][1] = 9

    htrc_results.add_cache(c1)
    htrc_results.add_cache(c2)
    htrc_results.add_cache(c3)

    Offset.gather_results(htrc_results.path)

    assert Offset.token_year_offset_count('token1', 1901, 1) == 1
    assert Offset.token_year_offset_count('token2', 1902, 1) == 2+4
    assert Offset.token_year_offset_count('token3', 1903, 1) == 3+5+7
    assert Offset.token_year_offset_count('token4', 1904, 1) == 6+8
    assert Offset.token_year_offset_count('token5', 1905, 1) == 9
