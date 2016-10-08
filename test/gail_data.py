

import os
import csv

from test.temp_dir import TempDir


class GailData(TempDir):

    def add_text(self, text):

        """
        Add a text to the corpus.

        Args:
            novel (Text)
        """

        fname = '{0}.xml'.format(text.identifier())

        path = os.path.join(self.path, fname)

        print(path)

        with open(path, 'w') as fh:
            print(text.tree, file=fh)
