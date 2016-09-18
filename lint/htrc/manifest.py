

import os
import numpy as np
import json

from lint.singletons import config


class Manifest:

    @classmethod
    def from_env(cls):

        """
        Wrap the ENV-defined manifest.

        Returns: cls
        """

        return cls(
            config['htrc']['features'],
            config['htrc']['manifest'],
        )

    def __init__(self, features_path, manifest_path):

        """
        Read and normalize the paths.

        Args:
            features_path (str)
            manifest_path (str)
        """

        # TODO: Use attrs module.

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
