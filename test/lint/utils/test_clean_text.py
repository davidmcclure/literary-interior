

import pytest

from lint.utils import clean_text


@pytest.mark.parametrize('text,clean', [

    # Trim whitespace.
    ('  text  ', 'text'),

    # Collapse 2+ spaces -> 1.
    ('a b  c   d    e', 'a b c d e'),

])
def test_clean_text(text, clean):
    assert clean_text(text) == clean
