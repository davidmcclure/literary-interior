

import pytest

from lint.singletons import session
from lint.count_cache import CountCache
from lint.models import Word

from test.factories.models import WordFactory


pytestmark = pytest.mark.usefixtures('db')


def test_delete_corpus():

    """
    Delete all counts for a corpus.
    """

    session.bulk_save_objects([
        WordFactory(corpus='c1'),
        WordFactory(corpus='c1'),
        WordFactory(corpus='c2'),
        WordFactory(corpus='c2'),
    ])

    Word.delete_corpus('c2')

    assert Word.query.filter_by(corpus='c1').count() == 2
    assert Word.query.filter_by(corpus='c2').count() == 0
