

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
        tokens=['one', 'two', 'three'],
        year=1910,
    )

    n2 = GailNovelFactory(
        year=1920,
        tokens=['four', 'five', 'six'],
    )

    n3 = GailNovelFactory(
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
            identifier=n1.id,
            year=1910,
            token='one',
            pos='CD',
            offset=0,
            ratio=0,
        )
        .exists()
        .scalar()
    )

    # assert TokenBin.get('gail', 1910, 'one',   'CD', o1) == 10
    # assert TokenBin.get('gail', 1910, 'two',   'CD', o2) == 10
    # assert TokenBin.get('gail', 1910, 'three', 'CD', o3) == 10

    # assert TokenBin.get('gail', 1920, 'four',  'CD', o1) == 20
    # assert TokenBin.get('gail', 1920, 'five',  'CD', o2) == 20
    # assert TokenBin.get('gail', 1920, 'six',   'CD', o3) == 20

    # assert TokenBin.get('gail', 1930, 'seven', 'CD', o1) == 30
    # assert TokenBin.get('gail', 1930, 'eight', 'CD', o2) == 30
    # assert TokenBin.get('gail', 1930, 'nine',  'CD', o3) == 30
