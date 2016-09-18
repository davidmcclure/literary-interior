

import os
import csv

from lint.utils import open_makedirs
from test.temp_dir import TempDir


class ChicagoData(TempDir):

    def texts_path(self):
        return os.path.join(self.path, 'Texts')

    def metadata_path(self):
        return os.path.join(self.path, 'NOVELS_METADATA.csv')

    def metadata_exists(self):
        return os.path.isfile(self.metadata_path())

    def add_novel(self, novel):

        """
        Add a novel to the corpus.

        Args:
            novel (ChicagoNovel)
        """

        # Add row to metadata CSV.

        first = not self.metadata_exists()

        row = novel.csv_row()

        writer = csv.DictWriter(
            open(self.metadata_path(), 'a'),
            row.keys(),
        )

        if first:
            writer.writeheader()

        writer.writerow(row)

        # Write text file.

        text_path = os.path.join(self.texts_path(), novel.filename())

        with open_makedirs(text_path, 'w') as fh:
            print(novel.text, file=fh)
