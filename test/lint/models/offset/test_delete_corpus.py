

import pytest

from lint.singletons import session
from lint.offset_cache import OffsetCache
from lint.models import Offset


pytestmark = pytest.mark.usefixtures('db')


def test_delete_corpus():

    """
    Delete all counts for a corpus.
    """

    session.bulk_save_objects([
        Offset(corpus='c1', token='token1', year=1900, offset=1, count=1),
        Offset(corpus='c1', token='token2', year=1900, offset=1, count=1),
        Offset(corpus='c2', token='token3', year=1900, offset=1, count=1),
        Offset(corpus='c2', token='token4', year=1900, offset=1, count=1),
    ])

    Offset.delete_corpus('c2')

    # Delete "c1" rows.
    assert Offset.query.filter_by(corpus='c1').count() == 2
    assert Offset.query.filter_by(corpus='c2').count() == 0
