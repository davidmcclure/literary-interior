

from test.factories.corpora.chicago import ChicagoNovelFactory


def test_source_text():

    """
    Return the entire text, when no Gutenberg header/footer.
    """

    text = """
    line1
    line2
    line3
    """

    novel = ChicagoNovelFactory(text=text)

    assert novel.source_text() == text


def test_strip_gutenberg_boilerplate():

    """
    Strip out the Gutenberg header/footer.
    """

    text = """
    line1
    line2
    line3
    *** START OF THIS PROJECT GUTENBERG EBOOK XXX ***
    line4
    line5
    line6
    *** END OF THIS PROJECT GUTENBERG EBOOK XXX ***
    line7
    line8
    line9
    """

    novel = ChicagoNovelFactory(text=text)

    assert novel.source_text() == """
    line4
    line5
    line6
    """
