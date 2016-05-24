

from test.helpers import make_page, make_vol


def test_token_count():

    """
    Volume#token_count should add up the body token counts for all pages.
    """

    v = make_vol(pages=[
        make_page(token_count=1),
        make_page(token_count=2),
        make_page(token_count=3),
    ])

    assert v.token_count == 1+2+3
