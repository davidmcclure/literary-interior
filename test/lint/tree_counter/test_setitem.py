

import pytest

from lint.tree_counter import TreeCounter


@pytest.mark.parametrize('path,count,tree', [

    # Single key

    (1, 2, {
        1: 2
    }),

    # Integer parts

    ((1, 2), 3, {
        1: {
            2: 3
        }
    }),

    ((1, 2, 3), 4, {
        1: {
            2: {
                3: 4
            }
        }
    }),

    # String parts

    (('a', 'b'), 3, {
        'a': {
            'b': 3
        }
    }),

    (('a', 'b', 'c'), 4, {
        'a': {
            'b': {
                'c': 4
            }
        }
    }),

    # Mixed parts

    ((1, 'b', 3), 4, {
        1: {
            'b': {
                3: 4
            }
        }
    }),

])
def test_setitem(path, count, tree):

    c = TreeCounter()

    c[path] = count
    assert c.tree == tree


def test_merge_shared_prefixes():

    c = TreeCounter()

    c[1,1,1] = 1
    c[1,1,2] = 2

    c[1,2,1] = 3
    c[1,2,2] = 4

    c[2,1,1] = 5
    c[2,1,2] = 6

    c[2,2,1] = 7
    c[2,2,2] = 8

    assert c.tree == {
        1: {
            1: {
                1: 1,
                2: 2,
            },
            2: {
                1: 3,
                2: 4,
            },
        },
        2: {
            1: {
                1: 5,
                2: 6,
            },
            2: {
                1: 7,
                2: 8,
            },
        },
    }


def test_override_subpath():

    c = TreeCounter()

    c[1,2,3] = 4
    c[1,2,3,4] = 5

    assert c.tree == {
        1: {
            2: {
                3: {
                    4: 5
                }
            }
        }
    }


def test_override_superpath():

    c = TreeCounter()

    c[1,2,3,4] = 5
    c[1,2,3] = 4

    assert c.tree == {
        1: {
            2: {
                3: 4
            }
        }
    }
