

import scandir
import os

from lint import config
from lint.volume import Volume
from lint.utils import grouper


# TODO: Use manifest.


class Corpus:

    @classmethod
    def from_env(cls):

        """
        Wrap the ENV-defined corpus root

        Returns: cls
        """

        return cls(config['corpus_dir'])

    def __init__(self, path):

        """
        Canonicalize the corpus path.

        Args:
            path (str)
        """

        self.path = os.path.abspath(path)

    def __len__(self):

        """
        How many volumes in the corpus?

        Returns: int
        """

        return len(list(self.paths()))

    def paths(self):

        """
        Generate asset paths.

        Yields: str
        """

        for root, dirs, files in scandir.walk(self.path):
            for name in files:
                yield os.path.join(root, name)

    def path_groups(self, n=1000):

        """
        Generate groups of paths.

        Yields: list
        """

        for group in grouper(self.paths(), n):
            yield group

    def volumes(self):

        """
        Generate volume instances.

        Yields: Volume
        """

        for path in self.paths():
            yield Volume.from_path(path)
