

import pytest

from subprocess import call

from lint.utils import make_offset
from lint.models import Char

from test.factories.corpora.gail import GailTextFactory


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_dump_offsets(gail_data):

    """
    ExtgailChars should index:
    (corpus, year, char, offset) -> count
    """

    for i in range(10):
        gail_data.add_text(GailTextFactory(
            year=1910,
            tokens=['abc'],
        ))

    for i in range(20):
        gail_data.add_text(GailTextFactory(
            year=1920,
            tokens=['def'],
        ))

    for i in range(30):
        gail_data.add_text(GailTextFactory(
            year=1930,
            tokens=['ghi'],
        ))

    call(['mpirun', 'bin/ext-gail-chars.py'])
    call(['bin/gather-gail-chars.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    assert Char.get('gail', 1910, 'a', o1) == 10
    assert Char.get('gail', 1910, 'b', o2) == 10
    assert Char.get('gail', 1910, 'c', o3) == 10

    assert Char.get('gail', 1920, 'd', o1) == 20
    assert Char.get('gail', 1920, 'e', o2) == 20
    assert Char.get('gail', 1920, 'f', o3) == 20

    assert Char.get('gail', 1930, 'g', o1) == 30
    assert Char.get('gail', 1930, 'h', o2) == 30
    assert Char.get('gail', 1930, 'i', o3) == 30


def test_round_years_to_decade(gail_data):

    """
    Volume years should be rounded to the nearest decade.
    """

    t1 = GailTextFactory(year=1904, tokens=['abc'])
    t2 = GailTextFactory(year=1905, tokens=['abc'])
    t3 = GailTextFactory(year=1906, tokens=['abc'])

    gail_data.add_text(t1)
    gail_data.add_text(t2)
    gail_data.add_text(t3)

    call(['mpirun', 'bin/ext-gail-chars.py'])
    call(['bin/gather-gail-chars.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    # n1 -> 1900
    assert Char.get('gail', 1900, 'a', o1) == 1
    assert Char.get('gail', 1900, 'b', o2) == 1
    assert Char.get('gail', 1900, 'c', o3) == 1

    # n2 + n3 -> 1910
    assert Char.get('gail', 1910, 'a', o1) == 2
    assert Char.get('gail', 1910, 'b', o2) == 2
    assert Char.get('gail', 1910, 'c', o3) == 2
