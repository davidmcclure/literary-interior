

import pytest

from subprocess import call

from lint.utils import make_offset
from lint.models import TokenBin

from test.factories.corpora.gail import GailTextFactory


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_dump_offsets(gail_data):

    """
    ExtractGail should index:
    (corpus, year, token, pos, offset) -> count
    """

    for i in range(10):
        gail_data.add_text(GailTextFactory(
            year=1910,
            tokens=['one', 'two', 'three'],
        ))

    for i in range(20):
        gail_data.add_text(GailTextFactory(
            year=1920,
            tokens=['four', 'five', 'six'],
        ))

    for i in range(30):
        gail_data.add_text(GailTextFactory(
            year=1930,
            tokens=['seven', 'eight', 'nine'],
        ))

    call(['mpirun', 'bin/ext-gail-tokens.py'])
    call(['bin/gather-gail-tokens.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    assert TokenBin.get('gail', 1910, 'one',   'CD', o1) == 10
    assert TokenBin.get('gail', 1910, 'two',   'CD', o2) == 10
    assert TokenBin.get('gail', 1910, 'three', 'CD', o3) == 10

    assert TokenBin.get('gail', 1920, 'four',  'CD', o1) == 20
    assert TokenBin.get('gail', 1920, 'five',  'CD', o2) == 20
    assert TokenBin.get('gail', 1920, 'six',   'CD', o3) == 20

    assert TokenBin.get('gail', 1930, 'seven', 'CD', o1) == 30
    assert TokenBin.get('gail', 1930, 'eight', 'CD', o2) == 30
    assert TokenBin.get('gail', 1930, 'nine',  'CD', o3) == 30


def test_round_years_to_decade(gail_data):

    """
    Volume years should be rounded to the nearest decade.
    """

    t1 = GailTextFactory(year=1904, tokens=['one', 'two', 'three'])
    t2 = GailTextFactory(year=1905, tokens=['one', 'two', 'three'])
    t3 = GailTextFactory(year=1906, tokens=['one', 'two', 'three'])

    gail_data.add_text(t1)
    gail_data.add_text(t2)
    gail_data.add_text(t3)

    call(['mpirun', 'bin/ext-gail-tokens.py'])
    call(['bin/gather-gail-tokens.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    # n1 -> 1900
    assert TokenBin.get('gail', 1900, 'one',   'CD', o1) == 1
    assert TokenBin.get('gail', 1900, 'two',   'CD', o2) == 1
    assert TokenBin.get('gail', 1900, 'three', 'CD', o3) == 1

    # n2 + n3 -> 1910
    assert TokenBin.get('gail', 1910, 'one',   'CD', o1) == 2
    assert TokenBin.get('gail', 1910, 'two',   'CD', o2) == 2
    assert TokenBin.get('gail', 1910, 'three', 'CD', o3) == 2
