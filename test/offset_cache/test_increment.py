

from lint.offset_cache import OffsetCache


def test_register_years():

    c = OffsetCache()

    c.increment(1901, {
        'token1': {
            1:1,
        },
    })

    c.increment(1902, {
        'token2': {
            2:2,
        },
    })

    assert c[1901]['token1'][1] == 1
    assert c[1902]['token2'][2] == 2


def test_register_tokens():

    c = OffsetCache()

    c.increment(1900, {
        'token1': {
            1:1,
        },
    })

    c.increment(1900, {
        'token2': {
            2:2,
        },
    })

    assert c[1900]['token1'][1] == 1
    assert c[1900]['token2'][2] == 2


def test_add_offsets():

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
            2:4,
            3:5,
            4:6,
        }
    })

    assert c[1900]['token'][1] == 1
    assert c[1900]['token'][2] == 2+4
    assert c[1900]['token'][3] == 3+5
    assert c[1900]['token'][4] == 6
