

from test.factories.htrc import HTRCPageFactory, HTRCVolumeFactory


def test_token_count():

    """
    Volume#token_count should add up the body token counts for all pages.
    """

    v = HTRCVolumeFactory(pages=[
        HTRCPageFactory(token_count=1),
        HTRCPageFactory(token_count=2),
        HTRCPageFactory(token_count=3),
    ])

    assert v.token_count() == 1+2+3
