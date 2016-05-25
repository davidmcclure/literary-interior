

import pickle

from lint.count_cache import CountCache


def test_write_pickle(mock_results):

    """
    CountCache#flush() should pickle the data to disk.
    """

    c1 = CountCache()
    c1[1900]['token'][1] = 1

    path = c1.flush(mock_results.path)

    with open(path, 'rb') as fh:
        c2 = pickle.load(fh)

    assert c2 == {
        1900: {
            'token': {
                1: 1
            }
        }
    }


def test_clear_data(mock_results):

    """
    After a flush, the cache should be cleared.
    """

    c = CountCache()
    c[1900]['token'][1] = 1

    path = c.flush(mock_results.path)

    assert len(c) == 0
