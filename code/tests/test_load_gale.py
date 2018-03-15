

import os
import pytest

from lint.jobs.load_gale import main
from lint.conn import spark
from tests.utils import read_yaml
from tests import FIXTURES_ROOT


# cases = read_yaml(__file__, 'test_load_gale.yml')


# SRC = os.path.join(FIXTURES_ROOT, 'chicago/gale')
# DEST = '/tmp/gale.parquet'


# @pytest.fixture(scope='module')
# def df():
    # """Run jobs, provide result.
    # """
    # main.callback(SRC, DEST)
    # return spark.read.parquet(DEST)


# @pytest.mark.parametrize('psmid,fields', cases.items())
# def test_load_chicago(df, psmid, fields):

    # row = df.filter(df.psmid == psmid).head()

    # text = fields.pop('text')
    # assert text in row.text.raw

    # for key, val in fields.items():
        # assert getattr(row, key) == val
