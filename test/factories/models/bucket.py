

import factory

from lint.models import Bucket


class BucketFactory(factory.Factory):

    class Meta:
        model = Bucket

    corpus = 'corpus'

    year = 1900

    token = 'token'

    pos = 'POS'

    offset = factory.Sequence(lambda n: n)

    count = 1
