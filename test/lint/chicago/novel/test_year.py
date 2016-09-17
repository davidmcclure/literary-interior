

import pytest

from lint.chicago.novel import Novel


@pytest.mark.parametrize('id,year', [
    (1, 1880),
    (3, 1880),
    (13, 1880),
])
def test_year(chicago_novel, id, year):

    novel = chicago_novel(id)

    assert novel.year() == year
