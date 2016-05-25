

from lint.count_cache import CountCache
from lint.models import Count


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
