

from collections import Counter

from lint.count_cache import CountCache


def test_add_new_paths():

    c = CountCache()

    c.add_char_counts(1901, Counter({
        ('a', 1): 1,
        ('b', 2): 2,
    }))

    c.add_char_counts(1902, Counter({
        ('c', 3): 3,
        ('d', 4): 4,
    }))

    assert c[1901, 'a', 1] == 1
    assert c[1901, 'b', 2] == 2

    assert c[1902, 'c', 3] == 3
    assert c[1902, 'd', 4] == 4


def test_update_existing_paths():

    c = CountCache()

    c.add_char_counts(1900, Counter({
        ('a', 1): 1,
        ('b', 2): 2,
    }))

    c.add_char_counts(1900, Counter({
        ('a', 1): 10,
        ('b', 2): 20,
    }))

    assert c[1900, 'a', 1] == 1+10
    assert c[1900, 'b', 2] == 2+20
