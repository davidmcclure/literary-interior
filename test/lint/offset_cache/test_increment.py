

from lint.tree_counter import TreeCounter
from lint.count_cache import CountCache


def test_add_new_paths():

    c = CountCache()

    c.increment(1901, TreeCounter({
        'token1': {
            'POS1': {
                1:1,
            },
        },
    }))

    c.increment(1902, TreeCounter({
        'token2': {
            'POS2': {
                2:2,
            },
        },
    }))

    assert c[1901, 'token1', 'POS1', 1] == 1
    assert c[1902, 'token2', 'POS2', 2] == 2


def test_update_existing_paths():

    c = CountCache()

    c.increment(1900, TreeCounter({
        'token': {
            'POS': {
                1:1,
            },
        },
    }))

    c.increment(1900, TreeCounter({
        'token': {
            'POS': {
                1:1,
            },
        },
    }))

    assert c[1900, 'token', 'POS', 1] == 2
