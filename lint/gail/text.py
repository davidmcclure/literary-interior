

import os

from bs4 import BeautifulSoup

from lint.utils import get_text


class Text:

    def __init__(self, path):

        """
        Parse the XML.

        Args:
            path (str)
        """

        self.path = os.path.abspath(path)

        with open(self.path, 'rb') as fh:
            self.xml = BeautifulSoup(fh, 'xml')

    def year(self):

        """
        Returns: int
        """

        return int(get_text(self.xml, 'pubDate pubDateStart')[:4])

    def plain_text(self):

        """
        Returns: str
        """

        words = self.xml.select('page[type="bodyPage"] wd')

        strings = [
            w.string
            for w in words
            if w.string
        ]

        return ' '.join(strings)
