

from bs4 import BeautifulSoup

from lint.utils import get_text


class Novel:

    @classmethod
    def from_path(cls, path):
        """Make an instance from an XML file.

        Args:
            path (str)
        """
        with open(path, 'rb') as fh:
            return cls(fh.read())

    def __init__(self, xml):
        """Parse the XML tree.

        Args:
            xml (str)
        """
        self.tree = BeautifulSoup(xml, 'xml')

    def identifier(self):
        """Returns: str
        """
        return get_text(self.tree, 'PSMID')

    def title(self):
        """Returns: str
        """
        return get_text(self.tree, 'titleGroup fullTitle')

    def author_first(self):
        """Returns: str
        """
        return get_text(self.tree, 'author first')

    def author_last(self):
        """Returns: str
        """
        return get_text(self.tree, 'author last')

    def year(self):
        """Returns: int
        """
        return int(get_text(self.tree, 'pubDate pubDateStart')[:4])

    def plain_text(self):
        """Returns: str
        """
        words = self.tree.select('page[type="bodyPage"] wd')

        strings = [
            w.string
            for w in words
            if w.string
        ]

        return ' '.join(strings)
