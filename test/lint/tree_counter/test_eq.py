

from lint.tree_counter import TreeCounter


def test_tree_counter():

    c1 = TreeCounter({1:2})
    c2 = TreeCounter({1:2})
    c3 = TreeCounter({1:3})

    assert c1 == c2
    assert not c1 == c3


def test_dict():

    c = TreeCounter({1:2})

    assert c == {1:2}
    assert not c == {1:3}
