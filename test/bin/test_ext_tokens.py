

import pytest

from subprocess import call

from lint.models import Text, Token
from lint.singletons import session

from test.factories.models import TextFactory


pytestmark = pytest.mark.usefixtures('mpi')


def test_ext_tokens():

    """
    ExtTokens should index token rows.
    """

    t1 = TextFactory(text='one two three')
    t2 = TextFactory(text='four five six')
    t3 = TextFactory(text='seven eight nine')

    session.add(t1)
    session.add(t2)
    session.add(t3)

    session.commit()

    call(['mpirun', 'bin/ext-tokens.py'])
    call(['bin/gather-tokens.py'])

    assert Token.query.count() == 9

    # TODO
