

import pytest

from lint.gail.text import Text


@pytest.mark.parametrize('path,year', [
    ('AMFCF0002-C00000-B0000400', 1849),
    ('AMFCF0002-C00000-B0000600', 1848),
    ('AMFCF0003-C00000-B0000100', 1913),
    ('AMFCF0003-C00000-B0000200', 1915),
])
def test_year(gail_fixture_path, path, year):

    text = Text(gail_fixture_path(path))

    assert text.year() == year
