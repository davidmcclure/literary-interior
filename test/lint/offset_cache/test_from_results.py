

from lint.offset_cache import OffsetCache


def test_from_results(htrc_results):

    """
    Merge together pickled instances.
    """

    c1 = OffsetCache()
    c1['token1', 1901, 1] = 1
    c1['token2', 1902, 1] = 2
    c1['token3', 1903, 1] = 3

    c2 = OffsetCache()
    c2['token2', 1902, 1] = 4
    c2['token3', 1903, 1] = 5
    c2['token4', 1904, 1] = 6

    c3 = OffsetCache()
    c3['token3', 1903, 1] = 7
    c3['token4', 1904, 1] = 8
    c3['token5', 1905, 1] = 9

    htrc_results.add_cache(c1)
    htrc_results.add_cache(c2)
    htrc_results.add_cache(c3)

    cache = OffsetCache.from_results(htrc_results.path)

    assert cache['token1', 1901, 1] == 1
    assert cache['token2', 1902, 1] == 2+4
    assert cache['token3', 1903, 1] == 3+5+7
    assert cache['token4', 1904, 1] == 6+8
    assert cache['token5', 1905, 1] == 9
