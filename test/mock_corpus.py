

import os
import json

from bz2 import compress

from test.temp_dir import TempDir


class MockCorpus(TempDir):

    def add_vol(self, vol):

        """
        Add a volume to the corpus.

        Args:
            vol (Volume)
        """

        path = os.path.join(self.path, '{0}.json.bz2'.format(vol.id))

        data = compress(json.dumps(vol.data).encode('utf8'))

        with open(path, 'wb') as fh:
            fh.write(data)
