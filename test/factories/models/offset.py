

import factory

from lint.models import Word


class WordFactory(factory.Factory):

    class Meta:
        model = Word

    corpus = 'corpus'

    year = 1900

    token = 'token'

    pos = 'POS'

    offset = factory.Sequence(lambda n: n)

    count = 1
