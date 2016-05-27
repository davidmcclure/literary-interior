

import pytest

from subprocess import call

from lint.models import Offset

from test.helpers import make_page, make_vol


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_dump_offsets():

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

    call(['mpirun', 'bin/dump_offsets'])

    Offset.gather_results()

    assert Offset.token_year_offset_count('a', 1900, round((50/300)*1000)) == 1
