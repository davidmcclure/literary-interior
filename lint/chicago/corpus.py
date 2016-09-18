

import csv
import os

from lint.singletons import config


class Corpus:

    @classmethod
    def from_env(cls):

        """
        Wrap the ENV-defined directory.

        Returns: cls
        """

        return cls(config['chicago'])

    def __init__(self, path):

        """
        Canonicalize the corpus path.

        Args:
            path (str)
        """

        self.path = os.path.abspath(path)

    def novels_metadata_path(self):

        """
        Get the path to `NOVELS_METADATA.csv`.

        Returns: str
        """

        return os.path.join(self.path, 'NOVELS_METADATA.csv')

    def novels_metadata(self):

        """
        Generate rows from the metadata CSV.

        Yields: dict
        """

        with open(self.novels_metadata_path(), 'r') as fh:
            yield from csv.DictReader(fh)
