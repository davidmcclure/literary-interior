

import os
import pickle
import uuid

from collections import defaultdict, Counter
from functools import partial

from lint.utils import flatten_dict


class OffsetCache:


    def __init__(self):

        """
        Initialize the {year -> token -> offset -> count} map.
        """

        self.data = defaultdict(partial(defaultdict, Counter))


    def __getitem__(self, year):

        """
        Alias indexing to the data dict.

        Args:
            year (int)

        Returns: dict
        """

        return self.data[year]


    def increment(self, year, token_offsets):

        """
        Increment token offsets for a year

        Args:
            year (int)
            token_offsets (dict)
        """

        for token, offsets in token_offsets.items():
            self.data[year][token] += offsets


    def flatten(self):

        """
        Flatten the cache into tuples.

        Yields: tuple (year, token, offset, count)
        """

        return flatten_dict(self.data)


    def flush(self, root):

        """
        Pickle the cache to a directory.

        Args:
            root (str)

        Returns: str
        """

        path = os.path.join(root, str(uuid.uuid4()))

        with open(path, 'wb') as fh:
            pickle.dump(self, fh)

        self.data.clear()

        return path
