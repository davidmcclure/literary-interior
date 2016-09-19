

import pytest

from subprocess import call

from lint.models import Offset

from test.utils import make_htrc_vol
from test.factories.htrc import HTRCPageFactory


pytestmark = pytest.mark.usefixtures('db', 'htrc_mpi')


def test_dump_offsets(htrc_data):

    """
    ExtractHTRC should index:
    (corpus, year, token, pos, offset) -> count
    """

    v1 = make_htrc_vol(year=1910, pages=[
        HTRCPageFactory(token_count=100, counts={'a': { 'POS1': 1 }}),
        HTRCPageFactory(token_count=100, counts={'b': { 'POS2': 2 }}),
        HTRCPageFactory(token_count=100, counts={'c': { 'POS3': 3 }}),
    ])

    v2 = make_htrc_vol(year=1920, pages=[
        HTRCPageFactory(token_count=100, counts={'b': { 'POS4': 4 }}),
        HTRCPageFactory(token_count=100, counts={'c': { 'POS5': 5 }}),
        HTRCPageFactory(token_count=100, counts={'d': { 'POS6': 6 }}),
    ])

    v3 = make_htrc_vol(year=1930, pages=[
        HTRCPageFactory(token_count=100, counts={'c': { 'POS7': 7 }}),
        HTRCPageFactory(token_count=100, counts={'d': { 'POS8': 8 }}),
        HTRCPageFactory(token_count=100, counts={'e': { 'POS9': 9 }}),
    ])

    htrc_data.add_vol(v1)
    htrc_data.add_vol(v2)
    htrc_data.add_vol(v3)

    call(['mpirun', 'bin/extract-htrc.py'])
    call(['bin/gather-htrc.py'])

    o1 = round(( 50/300)*100)
    o2 = round((150/300)*100)
    o3 = round((250/300)*100)

    assert Offset.get('htrc', 1910, 'a', 'POS1', o1) == 1
    assert Offset.get('htrc', 1910, 'b', 'POS2', o2) == 2
    assert Offset.get('htrc', 1910, 'c', 'POS3', o3) == 3

    assert Offset.get('htrc', 1920, 'b', 'POS4', o1) == 4
    assert Offset.get('htrc', 1920, 'c', 'POS5', o2) == 5
    assert Offset.get('htrc', 1920, 'd', 'POS6', o3) == 6

    assert Offset.get('htrc', 1930, 'c', 'POS7', o1) == 7
    assert Offset.get('htrc', 1930, 'd', 'POS8', o2) == 8
    assert Offset.get('htrc', 1930, 'e', 'POS9', o3) == 9


def test_ignore_non_english_volumes(htrc_data):

    """
    Non-English volumes should be skipped.
    """

    v1 = make_htrc_vol(year=1900, pages=[
        HTRCPageFactory(token_count=100, counts={'a': { 'POS': 1 }}),
        HTRCPageFactory(token_count=100, counts={'b': { 'POS': 2 }}),
        HTRCPageFactory(token_count=100, counts={'c': { 'POS': 3 }}),
    ])

    v2 = make_htrc_vol(year=1900, language='ger', pages=[
        HTRCPageFactory(token_count=100, counts={'a': { 'POS': 4 }}),
        HTRCPageFactory(token_count=100, counts={'b': { 'POS': 5 }}),
        HTRCPageFactory(token_count=100, counts={'c': { 'POS': 6 }}),
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


def test_round_years_to_decade(htrc_data):

    """
    Volume years should be rounded up to the nearest decade.
    """

    # <- 1900
    v1 = make_htrc_vol(year=1904, pages=[
        HTRCPageFactory(token_count=100, counts={'a': { 'POS': 2 }}),
        HTRCPageFactory(token_count=100, counts={'b': { 'POS': 4 }}),
        HTRCPageFactory(token_count=100, counts={'c': { 'POS': 8 }}),
    ])

    # -> 1910
    v2 = make_htrc_vol(year=1905, pages=[
        HTRCPageFactory(token_count=100, counts={'a': { 'POS': 16 }}),
        HTRCPageFactory(token_count=100, counts={'b': { 'POS': 32 }}),
        HTRCPageFactory(token_count=100, counts={'c': { 'POS': 64 }}),
    ])

    # -> 1910
    v3 = make_htrc_vol(year=1906, pages=[
        HTRCPageFactory(token_count=100, counts={'a': { 'POS': 128 }}),
        HTRCPageFactory(token_count=100, counts={'b': { 'POS': 256 }}),
        HTRCPageFactory(token_count=100, counts={'c': { 'POS': 512 }}),
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
