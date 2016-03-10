

import os


class Corpus:


    def __init__(self, path='corpus'):

        """
        Set the corpus path.
        """

        self.path = os.path.abspath(path)


    @property
    def paths(self):

        """
        Get .txt paths.

        Yields: str
        """

        for root, dirs, files in os.walk(self.path):
            for f in files:
                if f.endswith('.txt'):
                    yield os.path.join(root, f)
