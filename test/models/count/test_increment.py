

from lint import config
from lint.count_cache import CountCache
from lint.models import Count


def test_set_initial_value():

    """
    If a year/token/offset triple hasn't been seen before, insert a new row.
    """

    cache = CountCache()

    cache[1901]['token'][10] = 1
    cache[1902]['token'][10] = 2
    cache[1903]['token'][10] = 3

    Count.increment(cache)

    assert Count.token_year_offset_count('token', 1901, 10) == 1
    assert Count.token_year_offset_count('token', 1902, 10) == 2
    assert Count.token_year_offset_count('token', 1903, 10) == 3
