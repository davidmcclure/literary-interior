

from lint.utils import grouper


def test_even_groups():

    groups = grouper(range(50), 10)

    assert list(next(groups)) == list(range(10))
    assert list(next(groups)) == list(range(10, 20))
    assert list(next(groups)) == list(range(20, 30))
    assert list(next(groups)) == list(range(30, 40))
    assert list(next(groups)) == list(range(40, 50))


def test_uneven_groups():

    groups = grouper(range(55), 10)

    assert list(next(groups)) == list(range(10))
    assert list(next(groups)) == list(range(10, 20))
    assert list(next(groups)) == list(range(20, 30))
    assert list(next(groups)) == list(range(30, 40))
    assert list(next(groups)) == list(range(40, 50))
    assert list(next(groups)) == list(range(50, 55))
