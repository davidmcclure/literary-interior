

import pytest

from tests.utils import read_yaml


cases = read_yaml(__file__, 'cases.yml')


@pytest.mark.parametrize('psmid,fields', cases.items())
def test_load_gale(gale_df, psmid, fields):

    row = gale_df.filter(gale_df.psmid == psmid).head()

    for key, val in fields['metadata'].items():
        assert getattr(row, key) == val

    assert fields['text'] in row.text.raw
