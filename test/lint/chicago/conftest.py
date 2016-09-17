

import pytest
import os

from lint.chicago.corpus import Corpus
from lint.chicago.novel import Novel


@pytest.fixture
def chicago_novel(fixture_path):

    """
    Given a book id, provide a Novel instance.
    """

    def func(id):

        corpus = Corpus(fixture_path('chicago'))

        # Probe for the metadata row.
        for row in corpus.novels_metadata():
            if int(row['BOOK_ID']) == id:
                return Novel(corpus.path, row)

    return func
