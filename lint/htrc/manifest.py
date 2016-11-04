

import os


class Manifest:

    def __init__(self, features_path, manifest_path):

        """
        Read and normalize the paths.

        Args:
            features_path (str)
            manifest_path (str)
        """

        self.features_path = features_path
        self.manifest_path = manifest_path

    def absolute_paths(self):

        """
        Generate absolute paths to volume files.

        Yields: str
        """

        with open(self.manifest_path) as fh:
            for path in fh.read().splitlines():
                yield os.path.join(self.features_path, path)
