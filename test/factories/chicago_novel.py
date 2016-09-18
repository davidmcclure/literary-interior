

import factory

from schematics.models import Model
from schematics.types import IntType, StringType


class ChicagoNovel(Model):

    book_id = IntType(required=True)

    title = StringType(required=True)

    publ_date = IntType(required=True)

    text = StringType(required=True)

    def csv_row(self):

        """
        Build a metadata CSV row.
        """

        return dict(
            BOOK_ID=self.book_id,
            TITLE=self.title,
            PUBL_DATE=self.publ_date,
        )


class SchematicsFactory(factory.Factory):

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        """
        Pass the kwargs straight into the Schematics class.

        Returns: model_class
        """

        return model_class(kwargs)


class ChicagoNovelFactory(SchematicsFactory):

    class Meta:
        model = ChicagoNovel

    book_id = factory.Sequence(lambda n: n)

    title = 'Moby Dick'

    publ_date = 1900

    text = 'Call me Ishmael.'
