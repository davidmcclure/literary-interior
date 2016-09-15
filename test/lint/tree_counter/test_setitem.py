

import pytest

from lint.tree_counter import TreeCounter


@pytest.mark.parametrize('path,count', [

    # Single key
    (1, 2),

    # Integer parts
    ((1, 2), 3),
    ((1, 2, 3), 4),

    # String parts
    (('a', 'b'), 3),
    (('a', 'b', 'c'), 4),

])
def test_setitem(path, count):

    c = TreeCounter()

    c[path] = count
    assert c[path] == count
