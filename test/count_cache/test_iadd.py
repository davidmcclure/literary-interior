

from lint.count_cache import CountCache


def test_iadd():

    c1 = CountCache()

    c1[1901]['token1'][1] = 1
    c1[1902]['token2'][1] = 2
    c1[1903]['token3'][1] = 3

    c2 = CountCache()

    c2[1901]['token1'][1] = 11
    c2[1902]['token2'][1] = 22
    c2[1903]['token3'][1] = 33

    c1 += c2

    assert c1[1901]['token1'][1] == 1+11
    assert c1[1902]['token2'][1] == 2+22
    assert c1[1903]['token3'][1] == 3+33
