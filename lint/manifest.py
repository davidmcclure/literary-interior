

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

    def __init__(self, features_dir, manifest_path):

        """
        Read and normalize the paths.

        Args:
            features_dir (str)
            manifest_path (str)
        """

        with open(manifest_path, 'r') as fh:

            self.paths = [
                os.path.join(features_dir, path)
                for path in fh.read().splitlines()
            ]

    def json_segments(self, size):

        """
        Split the paths into a list of JSON-encoded segments.

        Args:
            size (int)
        """

        return [
            json.dumps(list(s))
            for s in np.array_split(self.paths, size)
        ]
