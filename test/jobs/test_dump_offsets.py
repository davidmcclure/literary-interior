

import pytest

from subprocess import call

from lint.models import Offset

from test.helpers import make_page, make_vol


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_dump_offsets(mock_corpus):

    v1 = make_vol(year=1901, pages=[
        make_page(token_count=100, counts={'a': { 'POS': 1 }}),
        make_page(token_count=100, counts={'b': { 'POS': 2 }}),
        make_page(token_count=100, counts={'c': { 'POS': 3 }}),
    ])

    v2 = make_vol(year=1902, pages=[
        make_page(token_count=100, counts={'b': { 'POS': 4 }}),
        make_page(token_count=100, counts={'c': { 'POS': 5 }}),
        make_page(token_count=100, counts={'d': { 'POS': 6 }}),
    ])

    v3 = make_vol(year=1903, pages=[
        make_page(token_count=100, counts={'c': { 'POS': 7 }}),
        make_page(token_count=100, counts={'d': { 'POS': 8 }}),
        make_page(token_count=100, counts={'e': { 'POS': 9 }}),
    ])

    mock_corpus.add_vol(v1)
    mock_corpus.add_vol(v2)
    mock_corpus.add_vol(v3)

    call(['mpirun', 'bin/dump-offsets'])

    Offset.gather_results()

    o1 = round(( 50/300)*1000)
    o2 = round((150/300)*1000)
    o3 = round((250/300)*1000)

    assert Offset.token_year_offset_count('a', 1901, o1) == 1
    assert Offset.token_year_offset_count('b', 1901, o2) == 2
    assert Offset.token_year_offset_count('c', 1901, o3) == 3

    assert Offset.token_year_offset_count('b', 1902, o1) == 4
    assert Offset.token_year_offset_count('c', 1902, o2) == 5
    assert Offset.token_year_offset_count('d', 1902, o3) == 6

    assert Offset.token_year_offset_count('c', 1903, o1) == 7
    assert Offset.token_year_offset_count('d', 1903, o2) == 8
    assert Offset.token_year_offset_count('e', 1903, o3) == 9
