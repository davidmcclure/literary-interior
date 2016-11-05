

from collections import Counter

from lint.count_cache import CountCache


def test_add_new_paths():

    c = CountCache()

    c.add_token_counts('corpus1', 1901, Counter({
        ('token1', 'POS1', 1): 1,
        ('token2', 'POS2', 2): 2,
    }))

    c.add_token_counts('corpus2', 1902, Counter({
        ('token3', 'POS3', 3): 3,
        ('token4', 'POS4', 4): 4,
    }))

    assert c['corpus1', 1901, 'token1', 'POS1', 1] == 1
    assert c['corpus1', 1901, 'token2', 'POS2', 2] == 2

    assert c['corpus2', 1902, 'token3', 'POS3', 3] == 3
    assert c['corpus2', 1902, 'token4', 'POS4', 4] == 4


def test_update_existing_paths():

    c = CountCache()

    c.add_token_counts('corpus', 1900, Counter({
        ('token1', 'POS1', 1): 1,
        ('token2', 'POS2', 2): 2,
    }))

    c.add_token_counts('corpus', 1900, Counter({
        ('token1', 'POS1', 1): 10,
        ('token2', 'POS2', 2): 20,
    }))

    assert c['corpus', 1900, 'token1', 'POS1', 1] == 1+10
    assert c['corpus', 1900, 'token2', 'POS2', 2] == 2+20
