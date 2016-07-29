

import os
import json

from bz2 import compress

from lint.utils import open_makedirs
from test.temp_dir import TempDir


class MockCorpus(TempDir):

    @property
    def features_path(self):
        return os.path.join(self.path, 'basic')

    @property
    def manifest_path(self):
        return os.path.join(self.path, 'pd-basic-file-listing.txt')

    def add_vol(self, vol):

        """
        Add a volume to the corpus.

        Args:
            vol (Volume)
        """

        path = os.path.join(
            self.features_path,
            '{0}.json.bz2'.format(vol.id),
        )

        data = compress(json.dumps(vol.data).encode('utf8'))

        with open_makedirs(path, 'wb') as fh:
            fh.write(data)
