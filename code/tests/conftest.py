

import findspark
findspark.init()

import os
import pytest

from lint.jobs import (
    load_gale,
    load_chicago_novels,
    load_chicago_authors,
    merge_novels,
)

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
def chicago_novels_df():
    """Load Chicago novels.
    """
    load_chicago_novels.main.callback(
        paths.CHICAGO_NOVELS_CSV_PATH,
        paths.CHICAGO_TEXT_DIR,
        paths.CHICAGO_NOVELS_DEST,
    )

    return spark.read.parquet(paths.CHICAGO_NOVELS_DEST)


@pytest.fixture(scope='module')
def chicago_authors_df():
    """Load Chicago authors.
    """
    load_chicago_authors.main.callback(
        paths.CHICAGO_AUTHORS_CSV_PATH,
        paths.CHICAGO_AUTHORS_DEST,
    )

    return spark.read.parquet(paths.CHICAGO_AUTHORS_DEST)


@pytest.fixture(scope='module')
def novels_df(gale_df, chicago_novels_df, chicago_authors_df):
    """Merge novels.
    """
    merge_novels.main.callback(
        paths.GALE_DEST,
        paths.CHICAGO_NOVELS_DEST,
        paths.CHICAGO_AUTHORS_DEST,
        paths.NOVELS_DEST,
    )

    return spark.read.parquet(paths.NOVELS_DEST)
