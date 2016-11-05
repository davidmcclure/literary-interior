

import pytest

from lint.singletons import session
from lint.count_cache import CountCache
from lint.models import Bucket

from test.factories.models import BucketFactory


pytestmark = pytest.mark.usefixtures('db')


def test_delete_corpus():

    """
    Delete all counts for a corpus.
    """

    session.bulk_save_objects([
        BucketFactory(corpus='c1'),
        BucketFactory(corpus='c1'),
        BucketFactory(corpus='c2'),
        BucketFactory(corpus='c2'),
    ])

    Bucket.delete_corpus('c2')

    assert Bucket.query.filter_by(corpus='c1').count() == 2
    assert Bucket.query.filter_by(corpus='c2').count() == 0
