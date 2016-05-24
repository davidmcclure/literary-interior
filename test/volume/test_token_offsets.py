

import pytest

from lint.volume import Volume

from test.helpers import make_page, make_vol


@pytest.mark.parametrize('r', [
    2,
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
            'b': {
                'POS': 2,
            },
            'c': {
                'POS': 3,
            },
        }),

        make_page(token_count=100, counts={
            'd': {
                'POS': 4,
            },
            'e': {
                'POS': 5,
            },
            'f': {
                'POS': 6,
            },
        }),

        make_page(token_count=100, counts={
            'g': {
                'POS': 7,
            },
            'h': {
                'POS': 8,
            },
            'i': {
                'POS': 9,
            },
        }),

    ])

    assert v.token_offsets(resolution=r) == {

        'a': {
            round((50/300) * r): 1
        },
        'b': {
            round((50/300) * r): 2
        },
        'c': {
            round((50/300) * r): 3
        },

        'd': {
            round((150/300) * r): 4
        },
        'e': {
            round((150/300) * r): 5
        },
        'f': {
            round((150/300) * r): 6
        },

        'g': {
            round((250/300) * r): 7
        },
        'h': {
            round((250/300) * r): 8
        },
        'i': {
            round((250/300) * r): 9
        },

    }
