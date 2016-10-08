

import os


class Novel:

    @classmethod
    def from_corpus_path(cls, corpus_path, metadata):

        """
        Hydrate a text instance from the corpus.

        Args:
            corpus_path (str)
            metadata (dict)
        """

        text_path = os.path.join(
            corpus_path,
            'Texts',
            metadata['FILENAME'],
        )

        with open(
            text_path,
            mode='r',
            encoding='utf8',
            errors='ignore',
        ) as fh:

            return cls(metadata, fh.read())

    def __init__(self, metadata, text):

        """
        Set the metadata and plain text.

        Args:
            metadata (dict)
            text (str)
        """

        self.metadata = metadata

        self.text = text

    def source_text(self):

        """
        Returns: str
        """

        # TODO: Strip out Gutenberg header/footer.

        return self.text

    def identifier(self):

        """
        Returns: str
        """

        return self.metadata['BOOK_ID']

    def title(self):

        """
        Returns: str
        """

        return self.metadata['TITLE']

    def year(self):

        """
        Returns: int
        """

        return int(self.metadata['PUBL_DATE'])
