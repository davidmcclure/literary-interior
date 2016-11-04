

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
        id='1',
        year=1910,
        tokens=['one', 'two', 'three'],
    )

    n2 = GailNovelFactory(
        id='2',
        year=1920,
        tokens=['four', 'five', 'six'],
    )

    n3 = GailNovelFactory(
        id='3',
        year=1930,
        tokens=['seven', 'eight', 'nine'],
    )

    gail_data.add_novel(n1)
    gail_data.add_novel(n2)
    gail_data.add_novel(n3)

    call(['mpirun', 'bin/ext-gail-tokens.py'])
    call(['bin/gather-gail-tokens.py'])

    assert (
        Token.query
        .filter_by(
            corpus='gail',
            identifier='1',
            year=1910,
            token='one',
            pos='CD',
            offset=0,
            ratio=0,
        )
        .count()
    ) == 1

    assert (
        Token.query
        .filter_by(
            corpus='gail',
            identifier='1',
            year=1910,
            token='two',
            pos='CD',
            offset=1,
            ratio=1/3,
        )
        .count()
    ) == 1
