

import factory

from schematics.models import Model
from schematics.types import IntType, StringType

from lint.chicago.novel import Novel


class ChicagoNovelFactory(factory.Factory):

    class Meta:
        model = Novel

    book_id = factory.Sequence(lambda n: n+1)

    title = 'Moby Dick'

    publ_date = 1900

    text = 'Call me Ishmael.'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        """
        Returns: Volume
        """

        file_id = str(kwargs['book_id']).zfill(8)

        # Generate the file name.
        filename = '{0}.txt'.format(file_id)

        # Construct the metadata row.
        metadata = dict(
            BOOK_ID=kwargs['book_id'],
            PUBL_DATE=kwargs['publ_date'],
            TITLE=kwargs['title'],
            FILENAME=filename,
        )

        return model_class(metadata, kwargs['text'])
