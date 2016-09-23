

import pytest

from subprocess import call

from lint.utils import make_offset
from lint.models import Offset

from test.factories.chicago import ChicagoNovelFactory


pytestmark = pytest.mark.usefixtures('db', 'chicago_mpi')


def test_dump_offsets(chicago_data):

    """
    ExtractChicago should index:
    (corpus, year, token, pos, offset) -> count
    """

    for i in range(10):
        chicago_data.add_novel(ChicagoNovelFactory(
            publ_date=1910,
            text='one two three',
        ))

    for i in range(20):
        chicago_data.add_novel(ChicagoNovelFactory(
            publ_date=1920,
            text='four five six',
        ))

    for i in range(30):
        chicago_data.add_novel(ChicagoNovelFactory(
            publ_date=1930,
            text='seven eight nine',
        ))

    call(['mpirun', 'bin/extract-chicago.py'])
    call(['bin/gather-chicago.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    assert Offset.get('chicago', 1910, 'one',   'CD', o1) == 10
    assert Offset.get('chicago', 1910, 'two',   'CD', o2) == 10
    assert Offset.get('chicago', 1910, 'three', 'CD', o3) == 10

    assert Offset.get('chicago', 1920, 'four',  'CD', o1) == 20
    assert Offset.get('chicago', 1920, 'five',  'CD', o2) == 20
    assert Offset.get('chicago', 1920, 'six',   'CD', o3) == 20

    assert Offset.get('chicago', 1930, 'seven', 'CD', o1) == 30
    assert Offset.get('chicago', 1930, 'eight', 'CD', o2) == 30
    assert Offset.get('chicago', 1930, 'nine',  'CD', o3) == 30


def test_round_years_to_decade(chicago_data):

    """
    Volume years should be rounded to the nearest decade.
    """

    n1 = ChicagoNovelFactory(publ_date=1904, text='one two three')
    n2 = ChicagoNovelFactory(publ_date=1905, text='one two three')
    n3 = ChicagoNovelFactory(publ_date=1906, text='one two three')

    chicago_data.add_novel(n1)
    chicago_data.add_novel(n2)
    chicago_data.add_novel(n3)

    call(['mpirun', 'bin/extract-chicago.py'])
    call(['bin/gather-chicago.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    # n1 -> 1900
    assert Offset.get('chicago', 1900, 'one',   'CD', o1) == 1
    assert Offset.get('chicago', 1900, 'two',   'CD', o2) == 1
    assert Offset.get('chicago', 1900, 'three', 'CD', o3) == 1

    # n2 + n3 -> 1910
    assert Offset.get('chicago', 1910, 'one',   'CD', o1) == 2
    assert Offset.get('chicago', 1910, 'two',   'CD', o2) == 2
    assert Offset.get('chicago', 1910, 'three', 'CD', o3) == 2
