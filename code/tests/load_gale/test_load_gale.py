

import pytest

from tests.utils import read_yaml


cases = read_yaml(__file__, 'cases.yml')


@pytest.mark.parametrize('psmid,fields', cases.items())
def test_load_chicago(gale_novels, psmid, fields):

    row = gale_novels.filter(gale_novels.psmid == psmid).head()

    for key, val in fields['metadata'].items():
        assert getattr(row, key) == val

    assert fields['text'] in row.text.raw
