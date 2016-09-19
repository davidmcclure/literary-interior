

from test.utils import make_htrc_vol
from test.factories.htrc import HTRCPageFactory


def test_token_count():

    """
    Volume#token_count should add up the body token counts for all pages.
    """

    v = make_htrc_vol(pages=[
        HTRCPageFactory(token_count=1),
        HTRCPageFactory(token_count=2),
        HTRCPageFactory(token_count=3),
    ])

    assert v.token_count() == 1+2+3
