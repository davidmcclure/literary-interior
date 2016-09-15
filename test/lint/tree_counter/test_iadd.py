

from lint.tree_counter import TreeCounter


def test_iadd():

    c1 = TreeCounter()
    c2 = TreeCounter()

    c1[1,1] = 1
    c1[1,2] = 2
    c1[1,3] = 3

    c2[1,2] = 7
    c2[1,3] = 8
    c2[1,4] = 9

    c1 += c2

    assert c1[1,1] == 1
    assert c1[1,2] == 2+7
    assert c1[1,3] == 3+8
    assert c1[1,4] == 9
