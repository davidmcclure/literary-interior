

import pytest
import os

from lint.chicago.corpus import Corpus
from lint.chicago.novel import Novel


@pytest.fixture
def chicago_fixture_path(fixture_path):

    """
    Provide the Chicago root path.
    """

    return fixture_path('chicago')


@pytest.fixture
def chicago_novel(chicago_fixture_path):

    """
    Given a book id, provide a Novel instance.
    """

    def func(id):

        corpus = Corpus(chicago_fixture_path)

        # Probe for the metadata row.
        for row in corpus.novels_metadata():
            if int(row['BOOK_ID']) == id:
                return Novel(chicago_fixture_path, row)

    return func
