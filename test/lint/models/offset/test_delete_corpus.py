

import pytest

from lint.singletons import session
from lint.offset_cache import OffsetCache
from lint.models import Offset

from test.factories import OffsetFactory


pytestmark = pytest.mark.usefixtures('db')


def test_delete_corpus():

    """
    Delete all counts for a corpus.
    """

    session.bulk_save_objects([
        OffsetFactory(corpus='c1'),
        OffsetFactory(corpus='c1'),
        OffsetFactory(corpus='c2'),
        OffsetFactory(corpus='c2'),
    ])

    Offset.delete_corpus('c2')

    assert Offset.query.filter_by(corpus='c1').count() == 2
    assert Offset.query.filter_by(corpus='c2').count() == 0
