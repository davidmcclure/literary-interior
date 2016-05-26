

from lint.offset_cache import OffsetCache


def test_merge_offsets():

    c = OffsetCache()

    c.increment(1900, {
        'token': {
            1:1,
            2:2,
            3:3,
        }
    })

    c.increment(1900, {
        'token': {
            1:4,
            2:5,
            3:6,
        }
    })

    assert c[1900]['token'][1] == 1+4
    assert c[1900]['token'][2] == 2+5
    assert c[1900]['token'][3] == 3+6
