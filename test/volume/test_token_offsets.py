

import pytest

from lint.volume import Volume

from test.helpers import make_page, make_vol


def test_map_page_center_offset_to_count():

    """
    For a token on a given page - get the offset of the "center" of the page,
    snap the offset onto a 1-N scale, and index the offset -> token count.
    """

    v = make_vol(pages=[

        make_page(token_count=100, counts={
            'a': {
                'POS': 1,
            }
        }),

        make_page(token_count=200, counts={
            'b': {
                'POS': 2,
            }
        }),

        make_page(token_count=300, counts={
            'c': {
                'POS': 3,
            }
        }),

    ])

    offsets = v.token_offsets(1000)

    assert offsets['a'][round(( 50/600)*1000)] == 1
    assert offsets['b'][round((200/600)*1000)] == 2
    assert offsets['c'][round((450/600)*1000)] == 3


@pytest.mark.parametrize('r', [
    10,
    100,
    1000,
])
def test_index_by_offset(r):

    """
    Each token should be mapped to a counter that maps offset -> count, where
    the offset is an integer between 0 (start) and N (end).
    """

    v = make_vol(pages=[

        make_page(token_count=100, counts={
            'a': {
                'POS': 1,
            },
        }),

        make_page(token_count=100, counts={
            'b': {
                'POS': 2,
            },
        }),

        make_page(token_count=100, counts={
            'c': {
                'POS': 3,
            },
        }),

    ])

    assert v.token_offsets(resolution=r) == {
        'a': {
            round(( 50/300) * r): 1
        },
        'b': {
            round((150/300) * r): 2
        },
        'c': {
            round((250/300) * r): 3
        },
    }


def test_merge_offsets_for_token():

    """
    Counts for different offsets for the same token should be merged under the
    key for the token.
    """

    v = make_vol(pages=[

        make_page(token_count=100, counts={
            'a': {
                'POS': 1,
            },
            'b': {
                'POS': 2,
            },
            'c': {
                'POS': 3,
            },
        }),

        make_page(token_count=100, counts={
            'b': {
                'POS': 4,
            },
            'c': {
                'POS': 5,
            },
            'd': {
                'POS': 6,
            },
        }),

        make_page(token_count=100, counts={
            'c': {
                'POS': 7,
            },
            'd': {
                'POS': 8,
            },
            'e': {
                'POS': 9,
            },
        }),

    ])

    assert v.token_offsets(1000) == {

        'a': {
            round(( 50/300) * 1000): 1,
        },

        'b': {
            round(( 50/300) * 1000): 2,
            round((150/300) * 1000): 4,
        },

        'c': {
            round(( 50/300) * 1000): 3,
            round((150/300) * 1000): 5,
            round((250/300) * 1000): 7,
        },

        'd': {
            round((150/300) * 1000): 6,
            round((250/300) * 1000): 8,
        },

        'e': {
            round((250/300) * 1000): 9,
        },

    }


def test_add_counts_when_offsets_round_together():

    """
    If a token appears on two pages, and the offsets for the two pages round to
    the same "tick" value, the counts should be added.
    """

    v = make_vol(pages=[

        make_page(token_count=100, counts={
            'a': {
                'POS': 1,
            },
        }),

        make_page(token_count=100, counts={
            'a': {
                'POS': 2,
            },
        }),

        make_page(token_count=100, counts={
            'a': {
                'POS': 3,
            },
        }),

        make_page(token_count=100, counts={
            'a': {
                'POS': 4,
            },
        }),

    ])

    offsets = v.token_offsets(4)

    assert offsets['a'][round(( 50/400) * 4)] == 1

    # Pages 2 and 3 both snap to offset 2.
    assert offsets['a'][round((150/400) * 4)] == 2+3
    assert offsets['a'][round((250/400) * 4)] == 2+3

    assert offsets['a'][round((350/400) * 4)] == 4
