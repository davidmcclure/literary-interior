

from lint.tree_counter import TreeCounter


def test_flatten():

    c = TreeCounter()

    c[1, 2, 3] = 1
    c[1, 2, 4] = 2
    c[1, 2, 5] = 3

    assert list(c.flatten()) == [
        ((1, 2, 3), 1),
        ((1, 2, 4), 2),
        ((1, 2, 5), 3),
    ]
