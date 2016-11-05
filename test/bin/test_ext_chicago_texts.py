

import pytest

from subprocess import call

from lint.models import Text

from test.factories.corpora.chicago import ChicagoNovelFactory


pytestmark = pytest.mark.usefixtures('db', 'mpi')


def test_ext_gail_texts(chicago_data):

    """
    ExttChicagoTexts should index text rows.
    """

    n1 = ChicagoNovelFactory(
        identifier='1',
        title='title1',
        author_first='first1',
        author_last='last1',
        year=1910,
        text='one two three',
    )

    n2 = ChicagoNovelFactory(
        identifier='2',
        title='title2',
        author_first='first2',
        author_last='last2',
        year=1920,
        text='four five six',
    )

    n3 = ChicagoNovelFactory(
        identifier='3',
        title='title3',
        author_first='first3',
        author_last='last3',
        year=1930,
        text='seven eight nine',
    )

    chicago_data.add_novel(n1)
    chicago_data.add_novel(n2)
    chicago_data.add_novel(n3)

    call(['mpirun', 'bin/ext-chicago-texts.py'])
    call(['bin/gather-texts.py'])

    t1 = Text.query.filter_by(corpus='chicago', identifier='1').one()
    t2 = Text.query.filter_by(corpus='chicago', identifier='2').one()
    t3 = Text.query.filter_by(corpus='chicago', identifier='3').one()

    assert t1.title == 'title1'
    assert t2.title == 'title2'
    assert t3.title == 'title3'

    assert t1.author_first == 'first1'
    assert t2.author_first == 'first2'
    assert t3.author_first == 'first3'

    assert t1.author_last == 'last1'
    assert t2.author_last == 'last2'
    assert t3.author_last == 'last3'

    assert t1.year == 1910
    assert t2.year == 1920
    assert t3.year == 1930

    assert t1.text == 'one two three'
    assert t2.text == 'four five six'
    assert t3.text == 'seven eight nine'
