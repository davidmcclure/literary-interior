

import os

from bs4 import BeautifulSoup

from lint.utils import get_text


class Text:

    @classmethod
    def from_path(cls, path):

        """
        Make an instance from an XML file.

        Args:
            path (str)
        """

        with open(path, 'rb') as fh:
            return cls(fh.read())

    def __init__(self, xml):

        """
        Parse the XML tree.

        Args:
            xml (str)
        """

        self.tree = BeautifulSoup(xml, 'xml')

    def year(self):

        """
        Returns: int
        """

        return int(get_text(self.tree, 'pubDate pubDateStart')[:4])

    def plain_text(self):

        """
        Returns: str
        """

        words = self.tree.select('page[type="bodyPage"] wd')

        strings = [
            w.string
            for w in words
            if w.string
        ]

        return ' '.join(strings)
