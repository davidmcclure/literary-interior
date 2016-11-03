

import pytest

from lint.singletons import session
from lint.count_cache import CountCache
from lint.models import TokenBin

from test.factories.models import TokenBinFactory


pytestmark = pytest.mark.usefixtures('db')


def test_delete_corpus():

    """
    Delete all counts for a corpus.
    """

    session.bulk_save_objects([
        TokenBinFactory(corpus='c1'),
        TokenBinFactory(corpus='c1'),
        TokenBinFactory(corpus='c2'),
        TokenBinFactory(corpus='c2'),
    ])

    TokenBin.delete_corpus('c2')

    assert TokenBin.query.filter_by(corpus='c1').count() == 2
    assert TokenBin.query.filter_by(corpus='c2').count() == 0
