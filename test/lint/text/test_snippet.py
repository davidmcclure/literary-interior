

from lint.text import Text


def test_snippet():

    text = Text('zero one two three four five six')

    prefix, token, suffix = text.snippet(3, padding=2)

    assert prefix   == 'one two '
    assert token    == 'three'
    assert suffix   == ' four five'


def test_left_overflow():

    text = Text('zero one two three four five six')

    prefix, token, suffix = text.snippet(2, padding=3)

    assert prefix   == 'zero one '
    assert token    == 'two'
    assert suffix   == ' three four five'


def test_right_overflow():

    text = Text('zero one two three four five six')

    prefix, token, suffix = text.snippet(4, padding=3)

    assert prefix   == 'one two three '
    assert token    == 'four'
    assert suffix   == ' five six'
