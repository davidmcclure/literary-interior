

import factory

from lint.chicago.novel import Novel


class ChicagoNovelFactory(factory.Factory):

    class Meta:
        model = Novel

    identifier = factory.Sequence(lambda n: n+1)

    title = 'Moby Dick'

    author_first = 'Herman'

    author_last = 'Melville'

    year = 1900

    text = 'Call me Ishmael.'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Returns: Volume
        """
        file_id = str(kwargs['identifier']).zfill(8)

        # Generate the file name.
        filename = '{0}.txt'.format(file_id)

        # Construct the metadata row.
        metadata = dict(
            BOOK_ID=kwargs['identifier'],
            TITLE=kwargs['title'],
            AUTH_FIRST=kwargs['author_first'],
            AUTH_LAST=kwargs['author_last'],
            PUBL_DATE=kwargs['year'],
            FILENAME=filename,
        )

        return model_class(metadata, kwargs['text'])
