

from lint.tree_counter import TreeCounter
from lint.offset_cache import OffsetCache


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

    assert c['token1', 1901, 1] == 1
    assert c['token2', 1902, 2] == 2


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

    assert c['token1', 1900, 1] == 1
    assert c['token2', 1900, 2] == 2


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

    assert c['token', 1900, 1] == 1
    assert c['token', 1900, 2] == 2+4
    assert c['token', 1900, 3] == 3+5
    assert c['token', 1900, 4] == 6
