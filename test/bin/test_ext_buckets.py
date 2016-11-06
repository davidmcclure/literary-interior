

import pytest

from subprocess import call

from lint.utils import make_offset
from lint.models import Bucket, Text
from lint.singletons import session

from test.factories.models import TextFactory


pytestmark = pytest.mark.usefixtures('mpi')


def test_ext_buckets():

    """
    ExtBuckets should index:
    (corpus, year, token, pos, offset) -> count
    """

    for i in range(10):

        session.add(TextFactory(
            corpus='corpus1',
            year=1910,
            text='one two three',
        ))

    for i in range(20):

        session.add(TextFactory(
            corpus='corpus2',
            year=1920,
            text='four five six',
        ))

    for i in range(30):

        session.add(TextFactory(
            corpus='corpus3',
            year=1930,
            text='seven eight nine',
        ))

    session.commit()

    call(['mpirun', 'bin/ext-buckets.py'])
    call(['bin/gather-buckets.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    assert Bucket.get('corpus1', 1910, 'one',   'CD', o1) == 10
    assert Bucket.get('corpus1', 1910, 'two',   'CD', o2) == 10
    assert Bucket.get('corpus1', 1910, 'three', 'CD', o3) == 10

    assert Bucket.get('corpus2', 1920, 'four',  'CD', o1) == 20
    assert Bucket.get('corpus2', 1920, 'five',  'CD', o2) == 20
    assert Bucket.get('corpus2', 1920, 'six',   'CD', o3) == 20

    assert Bucket.get('corpus3', 1930, 'seven', 'CD', o1) == 30
    assert Bucket.get('corpus3', 1930, 'eight', 'CD', o2) == 30
    assert Bucket.get('corpus3', 1930, 'nine',  'CD', o3) == 30


def test_round_years_to_decade():

    """
    Volume years should be rounded to the nearest decade.
    """

    session.add(TextFactory(
        corpus='corpus',
        year=1904,
        text='one two three',
    ))

    session.add(TextFactory(
        corpus='corpus',
        year=1905,
        text='one two three',
    ))

    session.add(TextFactory(
        corpus='corpus',
        year=1906,
        text='one two three',
    ))

    session.commit()

    call(['mpirun', 'bin/ext-buckets.py'])
    call(['bin/gather-buckets.py'])

    o1 = make_offset(0, 3, 100)
    o2 = make_offset(1, 3, 100)
    o3 = make_offset(2, 3, 100)

    # n1 -> 1900
    assert Bucket.get('corpus', 1900, 'one',   'CD', o1) == 1
    assert Bucket.get('corpus', 1900, 'two',   'CD', o2) == 1
    assert Bucket.get('corpus', 1900, 'three', 'CD', o3) == 1

    # n2 + n3 -> 1910
    assert Bucket.get('corpus', 1910, 'one',   'CD', o1) == 2
    assert Bucket.get('corpus', 1910, 'two',   'CD', o2) == 2
    assert Bucket.get('corpus', 1910, 'three', 'CD', o3) == 2
