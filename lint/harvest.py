

import os


class Harvest:


    def __init__(self, path='harvest'):

        """
        Set the corpus path.
        """

        self.path = os.path.abspath(path)


    @property
    def zip_paths(self):

        """
        Get .zip paths.

        Yields: str
        """

        for root, dirs, files in os.walk(self.path):
            for f in files:
                if f.endswith('.zip') and not f.endswith('-8.zip'):
                    yield os.path.join(root, f)
