

import factory

from lint.models import Token


class TokenFactory(factory.Factory):

    class Meta:
        model = Token

    corpus = 'corpus'

    year = 1900

    token = 'token'

    pos = 'POS'

    offset = factory.Sequence(lambda n: n)

    count = 1
