

import pytest

from subprocess import call

from lint.models import Offset

from test.helpers import make_page, make_vol


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_dump_offsets(mock_corpus):

    v1 = make_vol(year=1900, pages=[

        make_page(token_count=100, counts={
            'a': {
                'POS': 1
            }
        }),

        make_page(token_count=100, counts={
            'b': {
                'POS': 2
            }
        }),

        make_page(token_count=100, counts={
            'c': {
                'POS': 3
            }
        }),

    ])

    mock_corpus.add_vol(v1)

    call(['mpirun', 'bin/dump_offsets'])

    Offset.gather_results()

    o1 = round(( 50/300)*1000)
    o2 = round((150/300)*1000)
    o3 = round((250/300)*1000)

    assert Offset.token_year_offset_count('a', 1900, o1) == 1
    assert Offset.token_year_offset_count('b', 1900, o2) == 2
    assert Offset.token_year_offset_count('c', 1900, o3) == 3
