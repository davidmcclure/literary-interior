

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

    n3 = GailNovelFactory(
        psmid='3',
        year=1930,
        tokens=['seven', 'eight', 'nine'],
    )

    gail_data.add_novel(n1)
    gail_data.add_novel(n2)
    gail_data.add_novel(n3)

    call(['mpirun', 'bin/ext-gail-tokens.py'])
    call(['bin/gather-gail-tokens.py'])

    for i, token in enumerate(['one', 'two', 'three']):

        # assert Token.exists('gail', '1', token, 1910, 'CD', i, i/3)

        query = Token.query.filter_by(
            corpus='gail',
            identifier='1',
            year=1910,
            token=token,
            pos='CD',
            offset=i,
            ratio=i/3,
        )

        assert query.count() == 1
