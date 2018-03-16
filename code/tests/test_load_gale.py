

import os
import pytest

from lint.conn import spark
from lint.jobs.load_gale import main
from tests import FIXTURES_ROOT
from tests.utils import read_yaml


cases = read_yaml(__file__, 'gale.yml')


SRC = os.path.join(FIXTURES_ROOT, 'gale')
DEST = '/tmp/gale.parquet'


@pytest.fixture(scope='module')
def df():
    main.callback(SRC, DEST)
    return spark.read.parquet(DEST)


@pytest.mark.parametrize('psmid,fields', cases.items())
def test_load_chicago(df, psmid, fields):

    row = df.filter(df.psmid == psmid).head()

    assert fields['text'] in row.text.raw

    for key, val in fields['metadata'].items():
        assert getattr(row, key) == val
