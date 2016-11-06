

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

    t1 = TextFactory(text='t1 t2 t3')
    t2 = TextFactory(text='t4 t5 t6')
    t3 = TextFactory(text='t7 t8 t9')

    session.add(t1)
    session.add(t2)
    session.add(t3)

    session.commit()

    call(['mpirun', 'bin/ext-tokens.py'])
    call(['bin/gather-tokens.py'])

    for i, token in enumerate(['t1', 't2', 't3']):

        assert Token.query.filter_by(
            text=t1,
            token=token,
            pos='NN',
            char1=i*3,
            char2=i*3+2,
            offset=i,
            ratio=i/3,
        ).count() == 1

    for i, token in enumerate(['t4', 't5', 't6']):

        assert Token.query.filter_by(
            text=t2,
            token=token,
            pos='NN',
            char1=i*3,
            char2=i*3+2,
            offset=i,
            ratio=i/3,
        ).count() == 1

    for i, token in enumerate(['t7', 't8', 't9']):

        assert Token.query.filter_by(
            text=t3,
            token=token,
            pos='NN',
            char1=i*3,
            char2=i*3+2,
            offset=i,
            ratio=i/3,
        ).count() == 1
