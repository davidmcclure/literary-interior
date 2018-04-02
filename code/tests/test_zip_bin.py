

import pytest

from lint.utils import zip_bin


@pytest.mark.parametrize('seq,bin_count,bins', [

    (
        ['a', 'b', 'c', 'd', 'e', 'f'], 6,
        [0, 1, 2, 3, 4, 5],
    ),

    (
        ['a', 'b', 'c', 'd', 'e', 'f'], 3,
        [0, 0, 1, 1, 2, 2],
    ),

    (
        ['a', 'b', 'c', 'd', 'e', 'f'], 11,
        [0, 2, 4, 6, 8, 10],
    ),

])
def test_zip_bin(seq, bin_count, bins):
    assert list(zip_bin(seq, bin_count)) == list(zip(seq, bins))
