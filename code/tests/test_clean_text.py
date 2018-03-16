

import pytest

from lint.utils import clean_text


@pytest.mark.parametrize('text,clean', [

    # Trim.
    ('  text  ', 'text'),

    # 2+ spaces -> 1.
    ('a b  c   d    e', 'a b c d e'),

    # Linebreaks.
    ('a\nb', 'a b'),
    ('a\rb', 'a b'),
    ('a\tb', 'a b'),

    # 2+ linebreaks.
    ('a\n\nb', 'a b'),

])
def test_clean_text(text, clean):
    assert clean_text(text) == clean
