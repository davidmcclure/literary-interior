

from lint.htrc.page import Page

from test.utils import make_page


def test_add_pos_counts():

    """
    Page#merged_token_counts() should merged together POS-specific counts for
    each token.
    """

    p = make_page({
        'a': {
            'POS1': 1,
            'POS2': 2,
        },
        'b': {
            'POS1': 3,
            'POS2': 4,
        },
        'c': {
            'POS1': 5,
            'POS2': 6,
        },
    })

    assert p.merged_token_counts() == {
        'a': 1+2,
        'b': 3+4,
        'c': 5+6,
    }


def test_combine_casing_variants():

    """
    The same tokens with different casing should be combined.
    """

    p = make_page({
        'word': {
            'POS': 1,
        },
        'Word': {
            'POS': 2,
        },
    })

    assert p.merged_token_counts() == {
        'word': 1+2,
    }


def test_ignore_irregular_tokens():

    """
    Tokens that aren't [a-zA-Z] should be skipped.
    """

    p = make_page({

        'word': {
            'POS': 1,
        },

        # Number
        'word1': {
            'POS': 1,
        },

        # Punctuation
        '...': {
            'POS': 1,
        },

    })

    assert p.merged_token_counts() == {
        'word': 1,
    }
