

import pytest


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_dump_offsets():
    assert True
