

import pytest

from lint.count_cache import CountCache
from lint.models import Count


pytestmark = pytest.mark.usefixtures('db')


def test_test(mock_results):

    c1 = CountCache()
    c1[1901]['token1'][1] = 1
    c1[1902]['token2'][1] = 2
    c1[1903]['token3'][1] = 3

    c2 = CountCache()
    c2[1902]['token2'][1] = 4
    c2[1903]['token3'][1] = 5
    c2[1904]['token4'][1] = 6

    c3 = CountCache()
    c3[1903]['token3'][1] = 7
    c3[1904]['token4'][1] = 8
    c3[1905]['token5'][1] = 9

    mock_results.add_cache(c1)
    mock_results.add_cache(c2)
    mock_results.add_cache(c3)

    Count.gather_results(mock_results.path)

    assert Count.token_year_offset_count('token1', 1901, 1) == 1
    assert Count.token_year_offset_count('token2', 1902, 1) == 2+4
    assert Count.token_year_offset_count('token3', 1903, 1) == 3+5+7
    assert Count.token_year_offset_count('token4', 1904, 1) == 6+8
    assert Count.token_year_offset_count('token5', 1905, 1) == 9
