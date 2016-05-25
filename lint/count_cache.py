

import os
import pickle
import uuid

from collections import defaultdict, Counter
from functools import partial

from lint.utils import flatten_dict


class CountCache(defaultdict):


    def __init__(self, *args, **kwargs):

        """
        Initialize the {year -> token -> offset -> count} map.
        """

        super().__init__(partial(defaultdict, Counter))


    def __iadd__(self, other):

        """
        Merge another cache, adding the counters.

        Args:
            other (CountCache)
        """

        for year, token_counts in other.items():
            for token, counts in token_counts.items():
                self[year][token] += counts

        return self


    def flatten(self):

        """
        Flatten the cache into tuples.

        Yields: tuple (year, token, offset, count)
        """

        return flatten_dict(self)


    def flush(self, root):

        """
        Pickle the cache to a directory.

        Args:
            root (str)
        """

        path = os.path.join(root, str(uuid.uuid4()))

        with open(path, 'wb') as fh:
            pickle.dump(self, fh)
