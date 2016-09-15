

import pytest

from lint.utils import round_to_decade


@pytest.mark.parametrize('year,decade', [

    (1904, 1900),
    (1905, 1910),
    (1906, 1910),

    (1914, 1910),
    (1915, 1920),
    (1916, 1920),

])
def test_round_to_decade(year, decade):
    assert round_to_decade(year) == decade
