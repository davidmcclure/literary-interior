

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

        with open(text_path, encoding='utf8', errors='ignore') as fh:
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

    def author_first(self):

        """
        Returns: str
        """

        return self.metadata['AUTH_FIRST']

    def author_last(self):

        """
        Returns: str
        """

        return self.metadata['AUTH_LAST']

    def year(self):

        """
        Returns: int
        """

        return int(self.metadata['PUBL_DATE'])

    def plain_text(self):

        """
        Returns: str
        """

        i1 = None
        i2 = None

        lines = self.text.splitlines()

        tokens = ['***', 'PROJECT', 'GUTENBERG']

        for i, line in enumerate(lines):

            # Match "start" line.
            if False not in [
                token in line
                for token in tokens + ['START']
            ]:
                i1 = i+1

            # Match "end" line.
            if False not in [
                token in line
                for token in tokens + ['END']
            ]:
                i2 = i

        return '\n'.join(lines[i1:i2])
