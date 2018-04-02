

import pytest

from lint.utils import zip_offset


@pytest.mark.parametrize('seq,offsets', [
    (['a'], [0]),
    (['a', 'b'], [0, 1]),
    (['a', 'b', 'c'], [0, 0.5, 1]),
    (['a', 'b', 'c', 'd', 'e'], [0, 0.25, 0.5, 0.75, 1]),
])
def test_zip_offset(seq, offsets):
    assert list(zip_offset(seq)) == list(zip(seq, offsets))
