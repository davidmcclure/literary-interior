

from lint.offset_cache import OffsetCache


def test_iadd():

    c1 = OffsetCache()

    c1[1901]['token1'][1] = 1
    c1[1902]['token2'][2] = 2
    c1[1903]['token3'][3] = 3

    c2 = OffsetCache()

    c2[1902]['token2'][2] = 4
    c2[1903]['token3'][3] = 5
    c2[1904]['token4'][4] = 6

    c1 += c2

    assert c1[1901]['token1'][1] == 1
    assert c1[1902]['token2'][2] == 2+4
    assert c1[1903]['token3'][3] == 3+5
    assert c1[1904]['token4'][4] == 6
