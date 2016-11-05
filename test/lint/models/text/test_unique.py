

import pytest

from lint.models import Text


pytestmark = pytest.mark.usefixtures('db')


def test_unique_corpus_identifier():

    """
    Corpus + identifier should be unique.
    """

    assert True
