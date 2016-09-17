

import pytest

from lint.gail.text import Text


@pytest.mark.parametrize('path,head,tail', [

    (
        'AMFCF0002-C00000-B0000400',
        'THE DESPERADOES OF THE NEW WORLD. CHAPTER 1.',
        'even euch as Lney GaskelL—farewell, farewell.',
    ),

    (
        'AMFCF0002-C00000-B0000600',
        'AGNES; OR, THE POSSESSED: A REVELATION OF MESMERISM.',
        'and it cannot, therefore, have a good influence.',
    ),

    (
        'AMFCF0003-C00000-B0000100',
        'BRILLA CHAPTER I ίί\\/Έ5',
        'And the world is all at our feet.’ ”',
    ),

    (
        'AMFCF0003-C00000-B0000200',
        'VIRGINIA’S INHERITANCE VIRGINIA’S INHERITANCE CHAPTER I',
        'and the oil of joy for mourning.” THE END',
    ),

])
def test_year(gail_fixture_path, path, head, tail):

    text = Text(gail_fixture_path(path))

    plain_text = text.plain_text()

    assert plain_text.startswith(head)
    assert plain_text.endswith(tail)
