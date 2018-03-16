

import os
import pytest

from lint.conn import spark
from lint.jobs.load_chicago import main
from tests import FIXTURES_ROOT
from tests.utils import read_yaml


cases = read_yaml(__file__, 'cases.yml')


CSV_PATH = os.path.join(FIXTURES_ROOT, 'chicago/CHICAGO_NOVEL_CORPUS_METADATA/CHICAGO_CORPUS_NOVELS.csv')
TEXT_DIR = os.path.join(FIXTURES_ROOT, 'chicago/CHICAGO_NOVEL_CORPUS')
DEST = '/tmp/chicago.parquet'


@pytest.fixture(scope='module')
def df():
    main.callback(CSV_PATH, TEXT_DIR, DEST)
    return spark.read.parquet(DEST)


@pytest.mark.parametrize('book_id,fields', cases.items())
def test_load_chicago(df, book_id, fields):

    row = df.filter(df.book_id == book_id).head()

    for key, val in fields['metadata'].items():
        assert getattr(row, key) == val

    assert fields['text'] in row.text.raw
