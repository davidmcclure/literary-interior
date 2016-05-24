

import json
import bz2

from lint.page import Page


class Volume:


    @classmethod
    def from_path(cls, path):

        """
        Inflate a volume and make an instance.

        Args:
            path (str)

        Returns: cls
        """

        with bz2.open(path, 'rt') as fh:
            return cls(json.loads(fh.read()))


    def __init__(self, data):

        """
        Read the compressed volume archive.

        Args:
            data (dict)
        """

        self.data = data


    @property
    def id(self):

        """
        Get the HTRC id.

        Returns: str
        """

        return self.data['id']


    @property
    def year(self):

        """
        Get the publication year.

        Returns: int
        """

        return int(self.data['metadata']['pubDate'])


    @property
    def language(self):

        """
        Get the language.

        Returns: str
        """

        return self.data['metadata']['language']


    @property
    def is_english(self):

        """
        Is the volume English?

        Returns: bool
        """

        return self.language == 'eng'


    def token_count(self):

        """
        Get the total number of tokens in the page "body" sections.

        Returns: int
        """

        return sum([
            p.token_count
            for p in self.pages()
        ])


    def pages(self):

        """
        Generate page instances.

        Yields: Page
        """

        for data in self.data['features']['pages']:
            yield Page(data)


    def token_offsets(self, ticks=1000):

        """
        For each token, get the offsets of each instance of the token inside
        the text, with the offset is snapped onto an integer "tick."

        args:
            ticks (int)

        Returns: dict {token: Counter({ offset: count })}
        """

        pass
