

import os
import pickle
import uuid

from scandir import scandir
from collections import defaultdict, Counter
from functools import partial

from lint.utils import flatten_dict, mem_pct


# TODO: Subclass TreeCounter?

class OffsetCache(dict):

    @classmethod
    def from_results(cls, result_dir):

        """
        Merge together a set of pickled instances.

        Args:
            result_dir (str)
        """

        offsets = cls()

        # Gather pickle paths.
        paths = [
            d.path
            for d in scandir(result_dir)
            if d.is_file()
        ]

        # Walk paths.
        for i, path in enumerate(paths):
            with open(path, 'rb') as fh:

                # Merge offsets.
                offsets += pickle.load(fh)
                print(i, mem_pct())

        return offsets

    def __missing__(self, token):

        """
        Initialize the {token -> year -> offset -> count} map.
        """

        self[token] = defaultdict(Counter)

        return self[token]

    def __iadd__(self, other):

        """
        Merge in another offset cache.
        """

        for (token, year, offset), count in flatten_dict(other):
            self[token][year][offset] += count

        return self

    def increment(self, year, token_offsets):

        """
        Increment token offsets for a year.

        Args:
            year (int)
            token_offsets (TreeCounter)
        """

        for (token, pos, offset), count in token_offsets.flatten():
            self[token][year][offset] += count

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
