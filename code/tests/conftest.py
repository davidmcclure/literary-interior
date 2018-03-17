

import findspark
findspark.init()

import os
import pytest

from lint.conn import spark
from lint.jobs import load_gale, load_chicago, merge_novels
from . import paths


@pytest.fixture(scope='module')
def gale_novels():
    """Load Gale novels.
    """
    load_gale.main.callback(paths.GALE_SRC, paths.GALE_DEST)

    return spark.read.parquet(paths.GALE_DEST)


@pytest.fixture(scope='module')
def chicago_novels():
    """Load Chicago novels.
    """
    load_chicago.main.callback(
        paths.CHICAGO_CSV_PATH,
        paths.CHICAGO_TEXT_DIR,
        paths.CHICAGO_DEST,
    )

    return spark.read.parquet(paths.CHICAGO_DEST)


@pytest.fixture(scope='module')
def novels(gale_novels, chicago_novels):
    """Merge novels.
    """
    merge_novels.main.callback(
        paths.GALE_DEST,
        paths.CHICAGO_DEST,
        paths.NOVELS_DEST,
    )

    return spark.read.parquet(paths.NOVELS_DEST)
