

import pytest

from lint.singletons import session
from lint.count_cache import CountCache
from lint.models import Token

from test.factories.models import TokenFactory


pytestmark = pytest.mark.usefixtures('db')


def test_delete_corpus():

    """
    Delete all counts for a corpus.
    """

    session.bulk_save_objects([
        TokenFactory(corpus='c1'),
        TokenFactory(corpus='c1'),
        TokenFactory(corpus='c2'),
        TokenFactory(corpus='c2'),
    ])

    Token.delete_corpus('c2')

    assert Token.query.filter_by(corpus='c1').count() == 2
    assert Token.query.filter_by(corpus='c2').count() == 0
