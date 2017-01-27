

from lint.count_cache import CountCache


def test_from_results(bucket_results):
    """Merge together pickled instances.
    """
    c1 = CountCache()
    c1[1901, 'token1', 'POS1', 1] = 1
    c1[1902, 'token2', 'POS2', 1] = 2
    c1[1903, 'token3', 'POS3', 1] = 3

    c2 = CountCache()
    c2[1902, 'token2', 'POS2', 1] = 4
    c2[1903, 'token3', 'POS3', 1] = 5
    c2[1904, 'token4', 'POS4', 1] = 6

    c3 = CountCache()
    c3[1903, 'token3', 'POS3', 1] = 7
    c3[1904, 'token4', 'POS4', 1] = 8
    c3[1905, 'token5', 'POS5', 1] = 9

    bucket_results.add_cache(c1)
    bucket_results.add_cache(c2)
    bucket_results.add_cache(c3)

    cache = CountCache.from_results(bucket_results.path)

    assert cache[1901, 'token1', 'POS1', 1] == 1
    assert cache[1902, 'token2', 'POS2', 1] == 2+4
    assert cache[1903, 'token3', 'POS3', 1] == 3+5+7
    assert cache[1904, 'token4', 'POS4', 1] == 6+8
    assert cache[1905, 'token5', 'POS5', 1] == 9
