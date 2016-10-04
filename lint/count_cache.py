

import os
import pickle
import uuid

from scandir import scandir

from lint.utils import flatten_dict, mem_pct
from lint.tree_counter import TreeCounter


class CountCache(TreeCounter):

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

    def add_token_counts(self, year, counts):

        """
        Increment token counts:
        (token, pos, offset) -> count

        Args:
            year (int)
            counts (Counter)
        """

        for (token, pos, offset), count in counts.items():
            self[year, token, pos, offset] += count

    def add_char_counts(self, year, counts):

        """
        Increment character counts:
        (char, offset) -> count

        Args:
            counts (Counter)
        """

        for (char, offset), count in counts.items():
            self[year, char, offset] += count

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
