

import pytest

from subprocess import call

from lint.models import Offset

from test.utils import make_page, make_vol


pytestmark = pytest.mark.usefixtures('db', 'mpi')


# TODO: Test gather-results separately?


def test_dump_offsets(mock_corpus, mock_results):

    """
    DumpOffsets should index {token -> year -> offset -> count} data.
    """

    v1 = make_vol(year=1910, pages=[
        make_page(token_count=100, counts={'a': { 'POS': 1 }}),
        make_page(token_count=100, counts={'b': { 'POS': 2 }}),
        make_page(token_count=100, counts={'c': { 'POS': 3 }}),
    ])

    v2 = make_vol(year=1920, pages=[
        make_page(token_count=100, counts={'b': { 'POS': 4 }}),
        make_page(token_count=100, counts={'c': { 'POS': 5 }}),
        make_page(token_count=100, counts={'d': { 'POS': 6 }}),
    ])

    v3 = make_vol(year=1930, pages=[
        make_page(token_count=100, counts={'c': { 'POS': 7 }}),
        make_page(token_count=100, counts={'d': { 'POS': 8 }}),
        make_page(token_count=100, counts={'e': { 'POS': 9 }}),
    ])

    mock_corpus.add_vol(v1)
    mock_corpus.add_vol(v2)
    mock_corpus.add_vol(v3)

    call(['mpirun', 'bin/dump-offsets.py'])
    call(['bin/gather-results.py'])

    o1 = round(( 50/300)*100)
    o2 = round((150/300)*100)
    o3 = round((250/300)*100)

    assert Offset.token_year_offset_count('a', 1910, o1) == 1
    assert Offset.token_year_offset_count('b', 1910, o2) == 2
    assert Offset.token_year_offset_count('c', 1910, o3) == 3

    assert Offset.token_year_offset_count('b', 1920, o1) == 4
    assert Offset.token_year_offset_count('c', 1920, o2) == 5
    assert Offset.token_year_offset_count('d', 1920, o3) == 6

    assert Offset.token_year_offset_count('c', 1930, o1) == 7
    assert Offset.token_year_offset_count('d', 1930, o2) == 8
    assert Offset.token_year_offset_count('e', 1930, o3) == 9


def test_ignore_non_english_volumes(mock_corpus, mock_results):

    """
    Non-English volumes should be skipped.
    """

    v1 = make_vol(year=1900, pages=[
        make_page(token_count=100, counts={'a': { 'POS': 1 }}),
        make_page(token_count=100, counts={'b': { 'POS': 2 }}),
        make_page(token_count=100, counts={'c': { 'POS': 3 }}),
    ])

    v2 = make_vol(year=1900, language='ger', pages=[
        make_page(token_count=100, counts={'a': { 'POS': 4 }}),
        make_page(token_count=100, counts={'b': { 'POS': 5 }}),
        make_page(token_count=100, counts={'c': { 'POS': 6 }}),
    ])

    mock_corpus.add_vol(v1)
    mock_corpus.add_vol(v2)

    call(['mpirun', 'bin/dump-offsets.py'])
    call(['bin/gather-results.py'])

    o1 = round(( 50/300)*100)
    o2 = round((150/300)*100)
    o3 = round((250/300)*100)

    # Skip the German volume.
    assert Offset.token_year_offset_count('a', 1900, o1) == 1
    assert Offset.token_year_offset_count('b', 1900, o2) == 2
    assert Offset.token_year_offset_count('c', 1900, o3) == 3


def test_round_up_years_to_decade(mock_corpus, mock_results):

    """
    Volume years should be rounded up to the nearest decade.
    """

    # <- 1900
    v1 = make_vol(year=1904, pages=[
        make_page(token_count=100, counts={'a': { 'POS': 2 }}),
        make_page(token_count=100, counts={'b': { 'POS': 4 }}),
        make_page(token_count=100, counts={'c': { 'POS': 8 }}),
    ])

    # -> 1910
    v2 = make_vol(year=1905, pages=[
        make_page(token_count=100, counts={'a': { 'POS': 16 }}),
        make_page(token_count=100, counts={'b': { 'POS': 32 }}),
        make_page(token_count=100, counts={'c': { 'POS': 64 }}),
    ])

    # -> 1910
    v3 = make_vol(year=1906, pages=[
        make_page(token_count=100, counts={'a': { 'POS': 128 }}),
        make_page(token_count=100, counts={'b': { 'POS': 256 }}),
        make_page(token_count=100, counts={'c': { 'POS': 512 }}),
    ])

    mock_corpus.add_vol(v1)
    mock_corpus.add_vol(v2)
    mock_corpus.add_vol(v3)

    call(['mpirun', 'bin/dump-offsets.py'])
    call(['bin/gather-results.py'])

    o1 = round(( 50/300)*100)
    o2 = round((150/300)*100)
    o3 = round((250/300)*100)

    # Snap to decade.
    assert Offset.token_year_offset_count('a', 1900, o1) == 2
    assert Offset.token_year_offset_count('b', 1900, o2) == 4
    assert Offset.token_year_offset_count('c', 1900, o3) == 8

    assert Offset.token_year_offset_count('a', 1910, o1) == 16+128
    assert Offset.token_year_offset_count('b', 1910, o2) == 32+256
    assert Offset.token_year_offset_count('c', 1910, o3) == 64+512