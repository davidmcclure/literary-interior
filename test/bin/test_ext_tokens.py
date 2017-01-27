

import pytest

from subprocess import call

from lint.models import Text, Token
from lint.singletons import session

from test.factories.models import TextFactory


pytestmark = pytest.mark.usefixtures('mpi')


def test_ext_tokens():
    """ExtTokens should index token rows.
    """
    t1 = TextFactory(text='t01 t02 t03 t04')
    t2 = TextFactory(text='t05 t06 t07 t08')
    t3 = TextFactory(text='t09 t10 t11 t12')

    session.add(t1)
    session.add(t2)
    session.add(t3)

    session.commit()

    call(['mpirun', 'bin/ext-tokens.py'])
    call(['bin/gather-tokens.py'])

    for i, token in enumerate(['t01', 't02', 't03', 't04']):

        assert Token.query.filter_by(
            text=t1,
            token=token,
            pos='NN',
            char1=i*4,
            char2=i*4+3,
            offset=i,
            ratio=i/4,
        ).count() == 1

    for i, token in enumerate(['t05', 't06', 't07', 't08']):

        assert Token.query.filter_by(
            text=t2,
            token=token,
            pos='NN',
            char1=i*4,
            char2=i*4+3,
            offset=i,
            ratio=i/4,
        ).count() == 1

    for i, token in enumerate(['t09', 't10', 't11', 't12']):

        assert Token.query.filter_by(
            text=t3,
            token=token,
            pos='NN',
            char1=i*4,
            char2=i*4+3,
            offset=i,
            ratio=i/4,
        ).count() == 1
