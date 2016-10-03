

import factory

from schematics.models import Model
from schematics.types import IntType, StringType

from .schematics import SchematicsFactory


class ChicagoNovel(Model):

    book_id = IntType(required=True)

    title = StringType(required=True)

    publ_date = IntType(required=True)

    text = StringType(required=True)

    def filename(self):

        """
        Build the source text file name.

        Returns: str
        """

        return '{0}.txt'.format(str(self.book_id).zfill(8))

    def csv_row(self):

        """
        Build a metadata CSV row.

        Returns: dict
        """

        return dict(
            BOOK_ID=self.book_id,
            PUBL_DATE=self.publ_date,
            TITLE=self.title,
            FILENAME=self.filename(),
        )


class ChicagoNovelFactory(SchematicsFactory):

    class Meta:
        model = ChicagoNovel

    book_id = factory.Sequence(lambda n: n+1)

    title = 'Moby Dick'

    publ_date = 1900

    text = 'Call me Ishmael.'
