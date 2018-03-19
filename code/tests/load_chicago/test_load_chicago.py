

import pytest

from tests.utils import read_yaml


cases = read_yaml(__file__, 'cases.yml')


@pytest.mark.parametrize('book_id,fields', cases.items())
def test_load_chicago(chicago_df, book_id, fields):

    row = chicago_df.filter(chicago_df.book_id == book_id).head()

    for key, val in fields['metadata'].items():
        assert getattr(row, key) == val

    assert fields['text'] in row.text.raw