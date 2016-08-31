

import pytest

from lint import config
from lint.offset_cache import OffsetCache
from lint.models import Offset


pytestmark = pytest.mark.usefixtures('db')


def test_flush():

    """
    Insert a row for each year / token / offset / count.
    """

    cache = OffsetCache()

    cache[1901]['token1'][1] = 1
    cache[1902]['token2'][2] = 2
    cache[1903]['token3'][3] = 3

    Offset.flush(cache)

    assert Offset.token_year_offset_count('token1', 1901, 1) == 1
    assert Offset.token_year_offset_count('token2', 1902, 2) == 2
    assert Offset.token_year_offset_count('token3', 1903, 3) == 3
