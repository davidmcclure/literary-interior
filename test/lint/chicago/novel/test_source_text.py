

import pytest

from test.factories.corpora.chicago import ChicagoNovelFactory


headers = [
    '*** START OF THIS PROJECT GUTENBERG EBOOK ***',
    '***START OF THIS PROJECT GUTENBERG EBOOK***',
]


footers = [
    '*** END OF THIS PROJECT GUTENBERG EBOOK ***',
    '***END OF THIS PROJECT GUTENBERG EBOOK***',
]


def test_plain_text():
    """Return the entire text, when no Gutenberg header/footer.
    """
    text = '\n'.join([
        'line1',
        'line2',
        'line3',
    ])

    novel = ChicagoNovelFactory(text=text)

    assert novel.plain_text() == text


@pytest.mark.parametrize('header', headers)
def test_strip_gutenberg_header(header):
    """Strip out the Gutenberg header.
    """
    text = '\n'.join([
        'line1',
        'line2',
        'line3',
        header,
        'line4',
        'line5',
        'line6',
    ])

    novel = ChicagoNovelFactory(text=text)

    assert novel.plain_text() == '\n'.join([
        'line4',
        'line5',
        'line6',
    ])


@pytest.mark.parametrize('footer', footers)
def test_strip_gutenberg_footer(footer):
    """Strip out the Gutenberg footer.
    """
    text = '\n'.join([
        'line1',
        'line2',
        'line3',
        footer,
        'line4',
        'line5',
        'line6',
    ])

    novel = ChicagoNovelFactory(text=text)

    assert novel.plain_text() == '\n'.join([
        'line1',
        'line2',
        'line3',
    ])


@pytest.mark.parametrize('header,footer', zip(headers, footers))
def test_strip_gutenberg_header_and_footer(header, footer):
    """Strip out the Gutenberg header+footer.
    """
    text = '\n'.join([
        'line1',
        'line2',
        'line3',
        header,
        'line4',
        'line5',
        'line6',
        footer,
        'line7',
        'line8',
        'line9',
    ])

    novel = ChicagoNovelFactory(text=text)

    assert novel.plain_text() == '\n'.join([
        'line4',
        'line5',
        'line6',
    ])
