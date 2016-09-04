

from test.utils import make_htrc_page, make_htrc_vol


def test_token_count():

    """
    Volume#token_count should add up the body token counts for all pages.
    """

    v = make_htrc_vol(pages=[
        make_htrc_page(token_count=1),
        make_htrc_page(token_count=2),
        make_htrc_page(token_count=3),
    ])

    assert v.token_count() == 1+2+3
