

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

        corpus_path = fixture_path('chicago')

        corpus = Corpus(corpus_path)

        # Probe for the metadata row.
        for row in corpus.novels_metadata():
            if int(row['BOOK_ID']) == id:
                return Novel(corpus_path, row)

    return func
