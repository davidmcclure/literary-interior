

import pytest

from tests.utils import read_yaml


cases = read_yaml(__file__, 'cases.yml')


@pytest.mark.parametrize('fields', cases)
def test_merge_novels(novels, fields):

    row = (novels
        .filter(novels.corpus == fields['corpus'])
        .filter(novels.identifier == fields['identifier'])
        .head())

    for key, val in fields['metadata'].items():
        assert getattr(row, key) == val

    assert fields['text'] in row.text.raw
