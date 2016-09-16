

from collections import Counter

from lint.count_cache import CountCache


def test_add_new_paths():

    c = CountCache()

    c.add_volume(1901, Counter({
        ('token1', 'POS1', 1): 1
    }))

    c.add_volume(1902, Counter({
        ('token2', 'POS2', 2): 2
    }))

    assert c[1901, 'token1', 'POS1', 1] == 1
    assert c[1902, 'token2', 'POS2', 2] == 2


def test_update_existing_paths():

    c = CountCache()

    c.add_volume(1900, Counter({
        ('token', 'POS', 1): 1
    }))

    c.add_volume(1900, Counter({
        ('token', 'POS', 1): 1
    }))

    assert c[1900, 'token', 'POS', 1] == 2
