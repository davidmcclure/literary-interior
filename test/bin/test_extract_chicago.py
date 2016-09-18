

import pytest

from subprocess import call

from lint.models import Offset

from test.factories.chicago import ChicagoNovelFactory


pytestmark = pytest.mark.usefixtures('db', 'mpi')


@pytest.mark.skip
def test_dump_offsets(chicago_data, htrc_results):

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

    o1 = round((0/3)*100)
    o2 = round((1/3)*100)
    o3 = round((2/3)*100)

    assert Offset.get('chicago', 1910, 'one',   'CD', o1) == 10
    assert Offset.get('chicago', 1910, 'two',   'CD', o2) == 10
    assert Offset.get('chicago', 1910, 'three', 'CD', o3) == 10

    assert Offset.get('chicago', 1920, 'four',  'CD', o1) == 20
    assert Offset.get('chicago', 1920, 'five',  'CD', o2) == 20
    assert Offset.get('chicago', 1920, 'six',   'CD', o3) == 20

    assert Offset.get('chicago', 1930, 'seven', 'CD', o1) == 30
    assert Offset.get('chicago', 1930, 'eight', 'CD', o2) == 30
    assert Offset.get('chicago', 1930, 'nine',  'CD', o3) == 30


# def test_ignore_non_english_volumes(htrc_data, htrc_results):

    # """
    # Non-English volumes should be skipped.
    # """

    # v1 = make_htrc_vol(year=1900, pages=[
        # make_htrc_page(token_count=100, counts={'a': { 'POS': 1 }}),
        # make_htrc_page(token_count=100, counts={'b': { 'POS': 2 }}),
        # make_htrc_page(token_count=100, counts={'c': { 'POS': 3 }}),
    # ])

    # v2 = make_htrc_vol(year=1900, language='ger', pages=[
        # make_htrc_page(token_count=100, counts={'a': { 'POS': 4 }}),
        # make_htrc_page(token_count=100, counts={'b': { 'POS': 5 }}),
        # make_htrc_page(token_count=100, counts={'c': { 'POS': 6 }}),
    # ])

    # htrc_data.add_vol(v1)
    # htrc_data.add_vol(v2)

    # call(['mpirun', 'bin/extract-htrc.py'])
    # call(['bin/gather-htrc.py'])

    # o1 = round(( 50/300)*100)
    # o2 = round((150/300)*100)
    # o3 = round((250/300)*100)

    # # Skip the German volume.
    # assert Offset.get('htrc', 1900, 'a', 'POS', o1) == 1
    # assert Offset.get('htrc', 1900, 'b', 'POS', o2) == 2
    # assert Offset.get('htrc', 1900, 'c', 'POS', o3) == 3


# def test_round_years_to_decade(htrc_data, htrc_results):

    # """
    # Volume years should be rounded up to the nearest decade.
    # """

    # # <- 1900
    # v1 = make_htrc_vol(year=1904, pages=[
        # make_htrc_page(token_count=100, counts={'a': { 'POS': 2 }}),
        # make_htrc_page(token_count=100, counts={'b': { 'POS': 4 }}),
        # make_htrc_page(token_count=100, counts={'c': { 'POS': 8 }}),
    # ])

    # # -> 1910
    # v2 = make_htrc_vol(year=1905, pages=[
        # make_htrc_page(token_count=100, counts={'a': { 'POS': 16 }}),
        # make_htrc_page(token_count=100, counts={'b': { 'POS': 32 }}),
        # make_htrc_page(token_count=100, counts={'c': { 'POS': 64 }}),
    # ])

    # # -> 1910
    # v3 = make_htrc_vol(year=1906, pages=[
        # make_htrc_page(token_count=100, counts={'a': { 'POS': 128 }}),
        # make_htrc_page(token_count=100, counts={'b': { 'POS': 256 }}),
        # make_htrc_page(token_count=100, counts={'c': { 'POS': 512 }}),
    # ])

    # htrc_data.add_vol(v1)
    # htrc_data.add_vol(v2)
    # htrc_data.add_vol(v3)

    # call(['mpirun', 'bin/extract-htrc.py'])
    # call(['bin/gather-htrc.py'])

    # o1 = round(( 50/300)*100)
    # o2 = round((150/300)*100)
    # o3 = round((250/300)*100)

    # # Snap to decade.
    # assert Offset.get('htrc', 1900, 'a', 'POS', o1) == 2
    # assert Offset.get('htrc', 1900, 'b', 'POS', o2) == 4
    # assert Offset.get('htrc', 1900, 'c', 'POS', o3) == 8

    # assert Offset.get('htrc', 1910, 'a', 'POS', o1) == 16+128
    # assert Offset.get('htrc', 1910, 'b', 'POS', o2) == 32+256
    # assert Offset.get('htrc', 1910, 'c', 'POS', o3) == 64+512
