

import pickle

from lint.count_cache import CountCache


def test_write_pickle(bucket_results):
    """CountCache#flush() should pickle the data to disk.
    """
    c1 = CountCache()
    c1[1900, 'token', 'POS', 1] = 1

    path = c1.flush(bucket_results.path)

    with open(path, 'rb') as fh:
        c2 = pickle.load(fh)

    assert c2[1900, 'token', 'POS', 1] == 1
