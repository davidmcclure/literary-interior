

import pytest

from lint.utils import make_offset, token_offset_counts


def test_offset_counts():

    """
    Map (token, POS, offset) -> count.
    """

    counts = token_offset_counts('one two three four', 4)

    assert counts['one',    'CD', 0] == 1
    assert counts['two',    'CD', 1] == 1
    assert counts['three',  'CD', 2] == 1
    assert counts['four',   'CD', 3] == 1


@pytest.mark.parametrize('n', [10, 100, 1000])
def test_round_offsets(n):

    """
    When the offset is real-valued, round to the nearest integer.
    """

    counts = token_offset_counts('one two three four', n)

    o1 = make_offset(0, 4, n)
    o2 = make_offset(1, 4, n)
    o3 = make_offset(2, 4, n)
    o4 = make_offset(3, 4, n)

    assert counts['one',    'CD', o1] == 1
    assert counts['two',    'CD', o2] == 1
    assert counts['three',  'CD', o3] == 1
    assert counts['four',   'CD', o4] == 1


def test_downcase():

    """
    All tokens should be downcased.
    """

    counts = token_offset_counts('one Two THREE', 3)

    tokens = [k[0] for k in counts.keys()]

    assert set(tokens) == set(['one', 'two', 'three'])


def test_strip_tokens():

    """
    Strip non-[a-z] chars.
    """

    counts = token_offset_counts('.one .two .three .four', 4)

    tokens = [k[0] for k in counts.keys()]

    assert set(tokens) == set(['one', 'two', 'three', 'four'])
