

import pytest

from lint.utils import clean_token


@pytest.mark.parametrize('token,clean', [

    # Downcase.
    ('Token', 'token'),

    # Strip non-[a-z] chars.
    ('  "token!"  ', 'token'),

])
def test_clean_token(token, clean):
    assert clean_token(token) == clean
