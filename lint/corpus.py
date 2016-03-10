

import os


class Corpus:


    def __init__(self, path='corpus'):

        """
        Set the corpus path.
        """

        self.path = os.path.abspath(path)


    def paths(self, ext):

        """
        Get paths with a given extension.

        Args:
            ext (str)

        Yields: str
        """

        for root, dirs, files in os.walk(self.path):
            for f in files:
                if f.endswith(ext):
                    yield os.path.join(root, f)
