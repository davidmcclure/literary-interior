

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

    assert Token.query.filter_by(
        text=t1,
        token='one',
        pos='CD',
        char1=0,
        char2=3,
        offset=0,
        ratio=0/3,
    ).count() == 1

    assert Token.query.filter_by(
        text=t1,
        token='two',
        pos='CD',
        char1=4,
        char2=7,
        offset=1,
        ratio=1/3,
    ).count() == 1

    assert Token.query.filter_by(
        text=t1,
        token='three',
        pos='CD',
        char1=8,
        char2=13,
        offset=2,
        ratio=2/3,
    ).count() == 1
