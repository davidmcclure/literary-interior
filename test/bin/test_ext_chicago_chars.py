

import pytest

from subprocess import call

from lint.utils import make_offset
from lint.models import Char

from test.factories.corpora.chicago import ChicagoNovelFactory


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_dump_offsets(chicago_data):

    """
    ExtChicagoChars should index:
    (corpus, year, char, offset) -> count
    """

    for i in range(10):
        chicago_data.add_novel(ChicagoNovelFactory(
            publ_date=1910,
            text='abc',
        ))

    for i in range(20):
        chicago_data.add_novel(ChicagoNovelFactory(
            publ_date=1920,
            text='def',
        ))

    for i in range(30):
        chicago_data.add_novel(ChicagoNovelFactory(
            publ_date=1930,
            text='ghi',
        ))

    call(['mpirun', 'bin/ext-chicago-chars.py'])
    call(['bin/gather-chicago-chars.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    assert Char.get('chicago', 1910, 'a', o1) == 10
    assert Char.get('chicago', 1910, 'b', o2) == 10
    assert Char.get('chicago', 1910, 'c', o3) == 10

    assert Char.get('chicago', 1920, 'd', o1) == 20
    assert Char.get('chicago', 1920, 'e', o2) == 20
    assert Char.get('chicago', 1920, 'f', o3) == 20

    assert Char.get('chicago', 1930, 'g', o1) == 30
    assert Char.get('chicago', 1930, 'h', o2) == 30
    assert Char.get('chicago', 1930, 'i', o3) == 30


def test_round_years_to_decade(chicago_data):

    """
    Volume years should be rounded to the nearest decade.
    """

    n1 = ChicagoNovelFactory(publ_date=1904, text='abc')
    n2 = ChicagoNovelFactory(publ_date=1905, text='abc')
    n3 = ChicagoNovelFactory(publ_date=1906, text='abc')

    chicago_data.add_novel(n1)
    chicago_data.add_novel(n2)
    chicago_data.add_novel(n3)

    call(['mpirun', 'bin/ext-chicago-chars.py'])
    call(['bin/gather-chicago-chars.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    # n1 -> 1900
    assert Char.get('chicago', 1900, 'a', o1) == 1
    assert Char.get('chicago', 1900, 'b', o2) == 1
    assert Char.get('chicago', 1900, 'c', o3) == 1

    # n2 + n3 -> 1910
    assert Char.get('chicago', 1910, 'a', o1) == 2
    assert Char.get('chicago', 1910, 'b', o2) == 2
    assert Char.get('chicago', 1910, 'c', o3) == 2
