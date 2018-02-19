

from lxml import etree

from cached_property import cached_property

from . import fs
from .models import Token, GaleNovel


class GaleNovelXML:

    @classmethod
    def read(cls, path):
        return cls(etree.parse(fs.read(path)))

    def __init__(self, tree):
        self.tree = tree

    @cached_property
    def psmid(self):
        return self.tree.xpath('//PSMID/text()')[0]

    @cached_property
    def full_title(self):
        return self.tree.xpath('//fullTitle/text()')[0]

    @cached_property
    def author_first(self):
        return self.tree.xpath('//author/first/text()')[0]

    @cached_property
    def author_middle(self):
        return self.tree.xpath('//author/middle/text()')[0]

    @cached_property
    def author_last(self):
        return self.tree.xpath('//author/last/text()')[0]

    @cached_property
    def language(self):
        return self.tree.xpath('//language/text()')[0]

    @cached_property
    def pub_date_start(self):
        raw = self.tree.xpath('//pubDate/pubDateStart/text()')[0]
        return int(raw[:4])

    @cached_property
    def ocr(self):
        return float(self.tree.xpath('//ocr/text()')[0])

    @cached_property
    def text(self):
        tokens = self.tree.xpath('//page[@type="bodyPage"]//wd/text()')
        return ' '.join(tokens)

    @cached_property
    def tokens(self):
        return Token.parse(self.text)

    def row(self):
        """Assemble a DF row.

        Returns: GaleNovel
        """
        return GaleNovel(**{
            name: getattr(self, name)
            for name in GaleNovel.schema.names
        })
