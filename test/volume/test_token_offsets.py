

from lint.volume import Volume

from test.helpers import make_page, make_vol


def test_index_by_offset():

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

    assert v.token_offsets() == {

        'a': {
            round((50/300) * 1000): 1
        },
        'b': {
            round((50/300) * 1000): 2
        },
        'c': {
            round((50/300) * 1000): 3
        },

        'd': {
            round((150/300) * 1000): 4
        },
        'e': {
            round((150/300) * 1000): 5
        },
        'f': {
            round((150/300) * 1000): 6
        },

        'g': {
            round((250/300) * 1000): 7
        },
        'h': {
            round((250/300) * 1000): 8
        },
        'i': {
            round((250/300) * 1000): 9
        },

    }
