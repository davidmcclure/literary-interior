

import pytest

from subprocess import call

from lint.models import Token

from test.factories.corpora.gail import GailNovelFactory


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_dump_offsets(gail_data):

    """
    ExtGailTokens should index:
    (corpus, identifier, year, token, pos, offset, ratio)
    """

    n1 = GailNovelFactory(
        psmid='1',
        year=1910,
        tokens=['one', 'two', 'three'],
    )

    n2 = GailNovelFactory(
        psmid='2',
        year=1920,
        tokens=['four', 'five', 'six'],
    )

    gail_data.add_novel(n1)
    gail_data.add_novel(n2)

    call(['mpirun', 'bin/ext-gail-tokens.py'])
    call(['bin/gather-gail-tokens.py'])

    for i, token in enumerate(['one', 'two', 'three']):

        assert Token.exists(
            corpus='gail',
            identifier='1',
            year=1910,
            token=token,
            pos='CD',
            offset=i,
            ratio=i/3,
        )

    for i, token in enumerate(['four', 'five', 'six']):

        assert Token.exists(
            corpus='gail',
            identifier='2',
            year=1920,
            token=token,
            pos='CD',
            offset=i,
            ratio=i/3,
        )
