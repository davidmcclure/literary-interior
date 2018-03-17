

import pytest

from tests.utils import read_yaml


cases = read_yaml(__file__, 'cases.yml')


# @pytest.mark.parametrize('psmid,fields', cases.items())
def test_merge_novels(novels):
    assert novels.count() == 10
