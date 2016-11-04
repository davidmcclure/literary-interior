

import os

from lint.singletons import config
from lint.utils import scan_paths


class Corpus:

    def __init__(self, path):

        """
        Canonicalize the corpus path.

        Args:
            path (str)
        """

        self.path = os.path.abspath(path)

    def text_paths(self):

        """
        Generate paths to the XML sources.

        Yields: str
        """

        return scan_paths(self.path, '\.xml$')
