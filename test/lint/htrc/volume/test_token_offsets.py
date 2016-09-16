

import pytest

from lint.htrc.volume import Volume

from test.utils import make_htrc_page, make_htrc_vol


# TODO: Test POS branching.


@pytest.mark.parametrize('r', [
    10,
    100,
    1000,
])
def test_map_page_center_offset_to_count(r):

    """
    For a token on a given page - get the offset of the "center" of the page,
    snap the offset onto a 1-N scale, and index the offset -> token count.
    """

    v = make_htrc_vol(pages=[

        make_htrc_page(token_count=100, counts={
            'a': {
                'POS1': 1,
            }
        }),

        make_htrc_page(token_count=200, counts={
            'b': {
                'POS2': 2,
            }
        }),

        make_htrc_page(token_count=300, counts={
            'c': {
                'POS3': 3,
            }
        }),

    ])

    offsets = v.token_offsets(r)

    assert offsets['a', 'POS1', round(( 50/600)*r)] == 1
    assert offsets['b', 'POS2', round((200/600)*r)] == 2
    assert offsets['c', 'POS3', round((450/600)*r)] == 3


def test_merge_offsets_for_token():

    # TODO: What is this testing?

    """
    Counts for different offsets for the same token should be merged under the
    key for the token.
    """

    v = make_htrc_vol(pages=[

        make_htrc_page(token_count=100, counts={
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

        make_htrc_page(token_count=100, counts={
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

        make_htrc_page(token_count=100, counts={
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

    offsets = v.token_offsets(1000)

    assert offsets['a', 'POS1', round(( 50/300) * 1000)] == 1
    assert offsets['b', 'POS2', round(( 50/300) * 1000)] == 2
    assert offsets['c', 'POS3', round(( 50/300) * 1000)] == 3

    assert offsets['b', 'POS4', round((150/300) * 1000)] == 4
    assert offsets['c', 'POS5', round((150/300) * 1000)] == 5
    assert offsets['d', 'POS6', round((150/300) * 1000)] == 6

    assert offsets['c', 'POS7', round((250/300) * 1000)] == 7
    assert offsets['d', 'POS8', round((250/300) * 1000)] == 8
    assert offsets['e', 'POS9', round((250/300) * 1000)] == 9


def test_add_counts_when_offsets_round_together():

    """
    If a token appears on two pages, and the offsets for the two pages round to
    the same "tick" value, the counts should be added.
    """

    v = make_htrc_vol(pages=[

        make_htrc_page(token_count=100, counts={
            'a': {
                'POS': 1,
            },
        }),

        make_htrc_page(token_count=100, counts={
            'a': {
                'POS': 2,
            },
        }),

        make_htrc_page(token_count=100, counts={
            'a': {
                'POS': 3,
            },
        }),

        make_htrc_page(token_count=100, counts={
            'a': {
                'POS': 4,
            },
        }),

    ])

    offsets = v.token_offsets(4)

    assert offsets['a', 'POS', round(( 50/400) * 4)] == 1

    # Pages 2 and 3 both snap to offset 2.
    assert offsets['a', 'POS', round((150/400) * 4)] == 2+3
    assert offsets['a', 'POS', round((250/400) * 4)] == 2+3

    assert offsets['a', 'POS', round((350/400) * 4)] == 4
