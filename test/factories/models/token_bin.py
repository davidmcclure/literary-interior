

import factory

from lint.models import TokenBin


class TokenBinFactory(factory.Factory):

    class Meta:
        model = TokenBin

    corpus = 'corpus'

    year = 1900

    token = 'token'

    pos = 'POS'

    offset = factory.Sequence(lambda n: n)

    count = 1
