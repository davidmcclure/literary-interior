

import os
import ujson

from bz2 import compress

from lint.utils import open_makedirs
from test.temp_dir import TempDir


class HTRCData(TempDir):

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
            '{0}.ujson.bz2'.format(vol.id),
        )

        data = compress(ujson.dumps(vol.data).encode('utf8'))

        # Write the volume JSON.
        with open_makedirs(path, 'wb') as fh:
            fh.write(data)

        # Update the manifest.
        with open_makedirs(self.manifest_path, 'a') as fh:
            relpath = os.path.relpath(path, self.features_path)
            print(relpath, file=fh)
