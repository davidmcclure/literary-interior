

from lint.htrc.page import Page

from test.factories.htrc import HTRCPageFactory


def test_register_token_pos_counts():

    """
    Map token+POS -> count.
    """

    p = HTRCPageFactory(counts={
        'a': {
            'POS1': 1,
            'POS2': 2,
        },
        'b': {
            'POS3': 3,
            'POS4': 4,
        },
        'c': {
            'POS5': 5,
            'POS6': 6,
        },
    })

    assert p.token_pos_count() == {
        ('a', 'POS1'): 1,
        ('a', 'POS2'): 2,
        ('b', 'POS3'): 3,
        ('b', 'POS4'): 4,
        ('c', 'POS5'): 5,
        ('c', 'POS6'): 6,
    }


def test_combine_casing_variants():

    """
    The same tokens with different casing should be combined.
    """

    p = HTRCPageFactory(counts={
        'word': {
            'POS': 1,
        },
        'Word': {
            'POS': 2,
        },
    })

    assert p.token_pos_count() == {
        ('word', 'POS'): 1+2,
    }


def test_ignore_irregular_tokens():

    """
    Tokens that aren't [a-zA-Z] should be skipped.
    """

    p = HTRCPageFactory(counts={

        'word': {
            'POS': 1,
        },

        # Number
        'word1': {
            'POS': 2,
        },

        # Punctuation
        '...': {
            'POS': 3,
        },

    })

    assert p.token_pos_count() == {
        ('word', 'POS'): 1,
    }
