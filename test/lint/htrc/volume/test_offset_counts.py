

import pytest

from lint.utils import make_offset
from lint.htrc.volume import Volume

from test.factories.corpora.htrc import (
    HTRCPageFactory,
    HTRCVolumeFactory,
)


@pytest.mark.parametrize('r', [
    10,
    100,
    1000,
])
def test_use_page_center_as_offset(r):

    """
    For a token on a given page - get the offset of the "center" of the page,
    snap the offset onto a 1-N scale, and index the offset -> count.
    """

    v = HTRCVolumeFactory(pages=[

        HTRCPageFactory(token_count=100, counts={
            'a': {
                'POS1': 1,
            },
            'b': {
                'POS2': 2,
            },
            'c': {
                'POS3': 3,
            },
        }),

        HTRCPageFactory(token_count=200, counts={
            'b': {
                'POS4': 4,
            },
            'c': {
                'POS5': 5,
            },
            'd': {
                'POS6': 6,
            },
        }),

        HTRCPageFactory(token_count=300, counts={
            'c': {
                'POS7': 7,
            },
            'd': {
                'POS8': 8,
            },
            'e': {
                'POS9': 9,
            },
        }),

    ])

    offsets = v.offset_counts(r)

    o1 = make_offset( 50, 600, r)
    o2 = make_offset(200, 600, r)
    o3 = make_offset(450, 600, r)

    assert offsets['a', 'POS1', o1] == 1
    assert offsets['b', 'POS2', o1] == 2
    assert offsets['c', 'POS3', o1] == 3

    assert offsets['b', 'POS4', o2] == 4
    assert offsets['c', 'POS5', o2] == 5
    assert offsets['d', 'POS6', o2] == 6

    assert offsets['c', 'POS7', o3] == 7
    assert offsets['d', 'POS8', o3] == 8
    assert offsets['e', 'POS9', o3] == 9


def test_add_counts_when_offsets_round_together():

    """
    If a token appears on two pages, and the offsets for the two pages round to
    the same "tick" value, the counts should be added.
    """

    v = HTRCVolumeFactory(pages=[

        # center = 50
        HTRCPageFactory(token_count=100, counts={
            'a': {
                'POS': 1,
            },
        }),

        # center = 150
        HTRCPageFactory(token_count=100, counts={
            'a': {
                'POS': 2,
            },
        }),

        # center = 250
        HTRCPageFactory(token_count=100, counts={
            'a': {
                'POS': 3,
            },
        }),

        # center = 350
        HTRCPageFactory(token_count=100, counts={
            'a': {
                'POS': 4,
            },
        }),

    ])

    offsets = v.offset_counts(3)

    # ( 50/400)*3 -> 0.375 -> 0
    assert offsets['a', 'POS', 0] == 1

    # (150/400)*3 -> 1.125 -> 1
    # (250/400)*3 -> 1.875 -> 1
    assert offsets['a', 'POS', 1] == 2+3

    # (350/400)*3 -> 2.625 -> 2
    assert offsets['a', 'POS', 2] == 4
