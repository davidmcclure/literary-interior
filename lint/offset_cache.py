

import os
import pickle
import uuid

from collections import defaultdict, Counter
from functools import partial

from lint.utils import flatten_dict


class OffsetCache(dict):

    def __missing__(self, year):

        """
        Initialize the {year -> token -> offset -> count} map.
        """

        self[year] = defaultdict(Counter)

        return self[year]

    def __iadd__(self, other):

        """
        Merge in another offset cache.
        """

        for year, token, offset, count in flatten_dict(other):
            self[year][token][offset] += count

        return self

    def increment(self, year, token_offsets):

        """
        Increment token offsets for a year

        Args:
            year (int)
            token_offsets (dict)
        """

        for token, offsets in token_offsets.items():
            self[year][token] += offsets

    def flush(self, data_dir):

        """
        Pickle the cache to a directory.

        Args:
            data_dir (str)

        Returns: str
        """

        path = os.path.join(data_dir, str(uuid.uuid4()))

        with open(path, 'wb') as fh:
            pickle.dump(self, fh)

        return path
