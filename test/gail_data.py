

import os
import csv

from test.temp_dir import TempDir


class GailData(TempDir):

    def add_text(self, text):

        """
        Add a text to the corpus.

        Args:
            novel (GailText)
        """

        path = os.path.join(self.path, '{0}.xml'.format(text.id))

        with open(path, 'w') as fh:
            print(text.xml(), file=fh)
