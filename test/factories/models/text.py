

import factory

from lint.models import Text


class TextFactory(factory.Factory):

    class Meta:
        model = Text

    corpus = 'corpus'

    identifier = factory.Sequence(lambda n: str(n))

    title = 'Moby Dick'

    author_first = 'Herman'

    author_last = 'Melville'

    year = 1900

    text = 'Call me Ishmael.'
