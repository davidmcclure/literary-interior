

import pytest

from lint.utils import make_offset, char_offset_counts


def test_offset_counts():

    """
    Map (char, offset) -> count.
    """

    counts = char_offset_counts('abcd', 4)

    assert counts['a', 0] == 1
    assert counts['b', 1] == 1
    assert counts['c', 2] == 1
    assert counts['d', 3] == 1


@pytest.mark.parametrize('n', [10, 100, 1000])
def test_round_offsets(n):

    """
    When the offset is real-valued, round to the nearest integer.
    """

    counts = char_offset_counts('abcd', n)

    o1 = make_offset(0, 4, n)
    o2 = make_offset(1, 4, n)
    o3 = make_offset(2, 4, n)
    o4 = make_offset(3, 4, n)

    assert counts['a', o1] == 1
    assert counts['b', o2] == 1
    assert counts['c', o3] == 1
    assert counts['d', o4] == 1


def test_strip_text():

    """
    Leading / trailing whitespace should be ignored.
    """

    counts = char_offset_counts('  abcd  ', 4)

    assert counts['a', 0] == 1
    assert counts['b', 1] == 1
    assert counts['c', 2] == 1
    assert counts['d', 3] == 1


def test_collapse_whitespace():

    """
    2+ spaces should be collapsed to 1 space.
    """

    counts = char_offset_counts('ab  cd', 5)

    assert counts['a', 0] == 1
    assert counts['b', 1] == 1
    assert counts[' ', 2] == 1
    assert counts['c', 3] == 1
    assert counts['d', 4] == 1
