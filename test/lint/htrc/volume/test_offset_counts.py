

import pytest

from lint.htrc.volume import Volume

from test.utils import make_htrc_vol
from test.factories.htrc import HTRCPageFactory


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

    v = make_htrc_vol(pages=[

        HTRCPageFactory(token_count=100, token_pos_count={
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

        HTRCPageFactory(token_count=200, token_pos_count={
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

        HTRCPageFactory(token_count=300, token_pos_count={
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

    o1 = round(( 50/600)*r)
    o2 = round((200/600)*r)
    o3 = round((450/600)*r)

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

    v = make_htrc_vol(pages=[

        HTRCPageFactory(token_count=100, token_pos_count={
            'a': {
                'POS': 1,
            },
        }),

        HTRCPageFactory(token_count=100, token_pos_count={
            'a': {
                'POS': 2,
            },
        }),

        HTRCPageFactory(token_count=100, token_pos_count={
            'a': {
                'POS': 3,
            },
        }),

        HTRCPageFactory(token_count=100, token_pos_count={
            'a': {
                'POS': 4,
            },
        }),

    ])

    offsets = v.offset_counts(4)

    o1 = round(( 50/400)*4)
    o2 = round((150/400)*4)
    o3 = round((250/400)*4)
    o4 = round((350/400)*4)

    assert offsets['a', 'POS', o1] == 1

    # Pages 2 and 3 both snap to offset 2.
    assert offsets['a', 'POS', o2] == 2+3
    assert offsets['a', 'POS', o3] == 2+3

    assert offsets['a', 'POS', o4] == 4
