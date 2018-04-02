

import findspark
findspark.init()

import os
import pytest

from lint.jobs import load_gale, load_chicago, merge_novels
from lint.utils import get_spark

from . import paths


_, spark = get_spark()


@pytest.fixture(scope='module')
def gale_df():
    """Load Gale novels.
    """
    load_gale.main.callback(paths.GALE_SRC, paths.GALE_DEST)

    return spark.read.parquet(paths.GALE_DEST)


@pytest.fixture(scope='module')
def chicago_df():
    """Load Chicago novels.
    """
    load_chicago.main.callback(
        paths.CHICAGO_CSV_PATH,
        paths.CHICAGO_TEXT_DIR,
        paths.CHICAGO_DEST,
    )

    return spark.read.parquet(paths.CHICAGO_DEST)


@pytest.fixture(scope='module')
def novels_df(gale_df, chicago_df):
    """Merge novels.
    """
    merge_novels.main.callback(
        paths.GALE_DEST,
        paths.CHICAGO_DEST,
        paths.NOVELS_DEST,
    )

    return spark.read.parquet(paths.NOVELS_DEST)
