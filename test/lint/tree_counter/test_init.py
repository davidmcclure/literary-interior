

from lint.tree_counter import TreeCounter


def test_set_initial_tree():

    c = TreeCounter({
        1: {
            2: 3,
        }
    })

    assert c[1, 2] == 3
