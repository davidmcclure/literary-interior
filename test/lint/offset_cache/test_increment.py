

from lint.tree_counter import TreeCounter
from lint.offset_cache import OffsetCache


# TODO: Is this re-testing TreeCounter iadd?


def test_register_years():

    c = OffsetCache()

    c.increment(1901, TreeCounter({
        'token1': {
            'POS': {
                1:1,
            },
        },
    }))

    c.increment(1902, TreeCounter({
        'token2': {
            'POS': {
                2:2,
            },
        },
    }))

    assert c[1901, 'token1', 1] == 1
    assert c[1902, 'token2', 2] == 2


def test_register_tokens():

    c = OffsetCache()

    c.increment(1900, TreeCounter({
        'token1': {
            'POS': {
                1:1,
            },
        },
    }))

    c.increment(1900, TreeCounter({
        'token2': {
            'POS': {
                2:2,
            },
        },
    }))

    assert c[1900, 'token1', 1] == 1
    assert c[1900, 'token2', 2] == 2


def test_merge_offsets():

    c = OffsetCache()

    c.increment(1900, TreeCounter({
        'token': {
            'POS': {
                1:1,
                2:2,
                3:3,
            },
        },
    }))

    c.increment(1900, TreeCounter({
        'token': {
            'POS': {
                2:4,
                3:5,
                4:6,
            },
        },
    }))

    assert c[1900, 'token', 1] == 1
    assert c[1900, 'token', 2] == 2+4
    assert c[1900, 'token', 3] == 3+5
    assert c[1900, 'token', 4] == 6
