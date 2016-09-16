

import pickle

from lint.offset_cache import OffsetCache


def test_write_pickle(htrc_results):

    """
    OffsetCache#flush() should pickle the data to disk.
    """

    c1 = OffsetCache()
    c1['token', 1900, 1] = 1

    path = c1.flush(htrc_results.path)

    with open(path, 'rb') as fh:
        c2 = pickle.load(fh)

    assert c2['token', 1900, 1] == 1
