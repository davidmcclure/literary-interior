

import factory

from lint.models import Offset


class OffsetFactory(factory.Factory):

    class Meta:
        model = Offset

    corpus = 'corpus'

    year = 1900

    token = 'token'

    pos = 'POS'

    offset = factory.Sequence(lambda n: n)

    count = 1
