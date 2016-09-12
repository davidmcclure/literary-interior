

import factory

from lint.models import Offset


class OffsetFactory(factory.Factory):

    class Meta:
        model = Offset

    corpus = 'corpus'

    token = 'token'

    year = 1900

    offset = factory.Sequence(lambda n: n)

    count = 1
