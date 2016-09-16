

import pytest

from subprocess import call

from lint.models import Offset

from test.utils import make_htrc_page, make_htrc_vol


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_dump_offsets(htrc_data, htrc_results):

    """
    DumpOffsets should index {token -> year -> offset -> count} data.
    """

    v1 = make_htrc_vol(year=1910, pages=[
        make_htrc_page(token_count=100, counts={'a': { 'POS': 1 }}),
        make_htrc_page(token_count=100, counts={'b': { 'POS': 2 }}),
        make_htrc_page(token_count=100, counts={'c': { 'POS': 3 }}),
    ])

    v2 = make_htrc_vol(year=1920, pages=[
        make_htrc_page(token_count=100, counts={'b': { 'POS': 4 }}),
        make_htrc_page(token_count=100, counts={'c': { 'POS': 5 }}),
        make_htrc_page(token_count=100, counts={'d': { 'POS': 6 }}),
    ])

    v3 = make_htrc_vol(year=1930, pages=[
        make_htrc_page(token_count=100, counts={'c': { 'POS': 7 }}),
        make_htrc_page(token_count=100, counts={'d': { 'POS': 8 }}),
        make_htrc_page(token_count=100, counts={'e': { 'POS': 9 }}),
    ])

    htrc_data.add_vol(v1)
    htrc_data.add_vol(v2)
    htrc_data.add_vol(v3)

    call(['mpirun', 'bin/extract-htrc.py'])
    call(['bin/gather-htrc.py'])

    o1 = round(( 50/300)*100)
    o2 = round((150/300)*100)
    o3 = round((250/300)*100)

    assert Offset.get('htrc', 1910, 'a', 'POS', o1) == 1
    assert Offset.get('htrc', 1910, 'b', 'POS', o2) == 2
    assert Offset.get('htrc', 1910, 'c', 'POS', o3) == 3

    assert Offset.get('htrc', 1920, 'b', 'POS', o1) == 4
    assert Offset.get('htrc', 1920, 'c', 'POS', o2) == 5
    assert Offset.get('htrc', 1920, 'd', 'POS', o3) == 6

    assert Offset.get('htrc', 1930, 'c', 'POS', o1) == 7
    assert Offset.get('htrc', 1930, 'd', 'POS', o2) == 8
    assert Offset.get('htrc', 1930, 'e', 'POS', o3) == 9


def test_ignore_non_english_volumes(htrc_data, htrc_results):

    """
    Non-English volumes should be skipped.
    """

    v1 = make_htrc_vol(year=1900, pages=[
        make_htrc_page(token_count=100, counts={'a': { 'POS': 1 }}),
        make_htrc_page(token_count=100, counts={'b': { 'POS': 2 }}),
        make_htrc_page(token_count=100, counts={'c': { 'POS': 3 }}),
    ])

    v2 = make_htrc_vol(year=1900, language='ger', pages=[
        make_htrc_page(token_count=100, counts={'a': { 'POS': 4 }}),
        make_htrc_page(token_count=100, counts={'b': { 'POS': 5 }}),
        make_htrc_page(token_count=100, counts={'c': { 'POS': 6 }}),
    ])

    htrc_data.add_vol(v1)
    htrc_data.add_vol(v2)

    call(['mpirun', 'bin/extract-htrc.py'])
    call(['bin/gather-htrc.py'])

    o1 = round(( 50/300)*100)
    o2 = round((150/300)*100)
    o3 = round((250/300)*100)

    # Skip the German volume.
    assert Offset.get('htrc', 1900, 'a', 'POS', o1) == 1
    assert Offset.get('htrc', 1900, 'b', 'POS', o2) == 2
    assert Offset.get('htrc', 1900, 'c', 'POS', o3) == 3


def test_round_up_years_to_decade(htrc_data, htrc_results):

    """
    Volume years should be rounded up to the nearest decade.
    """

    # <- 1900
    v1 = make_htrc_vol(year=1904, pages=[
        make_htrc_page(token_count=100, counts={'a': { 'POS': 2 }}),
        make_htrc_page(token_count=100, counts={'b': { 'POS': 4 }}),
        make_htrc_page(token_count=100, counts={'c': { 'POS': 8 }}),
    ])

    # -> 1910
    v2 = make_htrc_vol(year=1905, pages=[
        make_htrc_page(token_count=100, counts={'a': { 'POS': 16 }}),
        make_htrc_page(token_count=100, counts={'b': { 'POS': 32 }}),
        make_htrc_page(token_count=100, counts={'c': { 'POS': 64 }}),
    ])

    # -> 1910
    v3 = make_htrc_vol(year=1906, pages=[
        make_htrc_page(token_count=100, counts={'a': { 'POS': 128 }}),
        make_htrc_page(token_count=100, counts={'b': { 'POS': 256 }}),
        make_htrc_page(token_count=100, counts={'c': { 'POS': 512 }}),
    ])

    htrc_data.add_vol(v1)
    htrc_data.add_vol(v2)
    htrc_data.add_vol(v3)

    call(['mpirun', 'bin/extract-htrc.py'])
    call(['bin/gather-htrc.py'])

    o1 = round(( 50/300)*100)
    o2 = round((150/300)*100)
    o3 = round((250/300)*100)

    # Snap to decade.
    assert Offset.get('htrc', 1900, 'a', 'POS', o1) == 2
    assert Offset.get('htrc', 1900, 'b', 'POS', o2) == 4
    assert Offset.get('htrc', 1900, 'c', 'POS', o3) == 8

    assert Offset.get('htrc', 1910, 'a', 'POS', o1) == 16+128
    assert Offset.get('htrc', 1910, 'b', 'POS', o2) == 32+256
    assert Offset.get('htrc', 1910, 'c', 'POS', o3) == 64+512
