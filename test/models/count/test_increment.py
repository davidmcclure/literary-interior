

import pytest

from lint import config
from lint.count_cache import CountCache
from lint.models import Count


pytestmark = pytest.mark.usefixtures('db')


def test_set_initial_value():

    """
    If a year/token/offset triple hasn't been seen before, insert a new row.
    """

    cache = CountCache()

    cache[1901]['token1'][1] = 1
    cache[1902]['token2'][2] = 2
    cache[1903]['token3'][3] = 3

    Count.increment(cache)

    assert Count.token_year_offset_count('token1', 1901, 1) == 1
    assert Count.token_year_offset_count('token2', 1902, 2) == 2
    assert Count.token_year_offset_count('token3', 1903, 3) == 3


def test_increment_existing_value():

    """
    If a year/token/offset triple is already in the database, increment the
    count for the existing row.
    """

    cache = CountCache()

    cache[1901]['token1'][1] = 1
    cache[1902]['token2'][2] = 2
    cache[1903]['token3'][3] = 3

    Count.increment(cache)

    cache[1901]['token1'][1] = 4
    cache[1902]['token2'][2] = 5
    cache[1903]['token3'][3] = 6

    Count.increment(cache)

    assert Count.token_year_offset_count('token1', 1901, 1) == 1+4
    assert Count.token_year_offset_count('token2', 1902, 2) == 2+5
    assert Count.token_year_offset_count('token3', 1903, 3) == 3+6
