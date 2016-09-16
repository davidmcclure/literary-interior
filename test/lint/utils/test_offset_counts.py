

from lint.utils import offset_counts


def test_offset_counts():

    counts = offset_counts('one two three four', 4)

    assert counts['one', 'CD', 0] == 1
    assert counts['two', 'CD', 1] == 1
    assert counts['three', 'CD', 2] == 1
    assert counts['four', 'CD', 3] == 1
