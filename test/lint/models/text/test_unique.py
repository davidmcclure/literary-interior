

import pytest

from sqlalchemy.exc import IntegrityError

from lint.singletons import session

from test.factories.models import TextFactory


pytestmark = pytest.mark.usefixtures('db')


def test_unique_corpus_identifier():
    """Corpus + identifier should be unique.
    """
    t1 = TextFactory(corpus='corpus', identifier='1')
    t2 = TextFactory(corpus='corpus', identifier='1')

    session.add(t1)
    session.add(t2)

    with pytest.raises(IntegrityError):
        session.commit()
