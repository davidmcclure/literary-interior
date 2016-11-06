

from lint.models import Text


def test_snippet():

    text = Text(text='0123456')

    prefix, token, suffix = text.snippet(2, 5, padding=2)

    assert prefix   == '01'
    assert token    == '234'
    assert suffix   == '56'


def test_overflow():

    text = Text(text='0123456')

    prefix, token, suffix = text.snippet(2, 5, padding=20)

    assert prefix   == '01'
    assert token    == '234'
    assert suffix   == '56'
