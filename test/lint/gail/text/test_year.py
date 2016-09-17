

import pytest

from lint.gail.text import Text


@pytest.mark.parametrize('path,year', [
    ('gail-amfic/AMFCF0002-C00000/Monographs/AMFCF0002-C00000-B0000400.xml', 1849),
    ('gail-amfic/AMFCF0002-C00000/Monographs/AMFCF0002-C00000-B0000600.xml', 1848),
    ('gail-amfic/AMFCF0003-C00000/Monographs/AMFCF0003-C00000-B0000100.xml', 1913),
    ('gail-amfic/AMFCF0003-C00000/Monographs/AMFCF0003-C00000-B0000200.xml', 1915),
])
def test_year(fixture_path, path, year):

    text = Text(fixture_path(path))

    assert text.year() == year
