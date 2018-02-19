

from lxml import etree

from . import fs
from .models import Token, GaleNovel


class GaleNovelXML:

    @classmethod
    def read(cls, path):
        return cls(etree.parse(fs.read(path)))

    def __init__(self, tree):
        self.tree = tree

    def psmid(self):
        return self.tree.xpath('//PSMID/text()')[0]

    def full_title(self):
        return self.tree.xpath('//fullTitle/text()')[0]

    def author_first(self):
        return self.tree.xpath('//author/first/text()')[0]

    def author_middle(self):
        return self.tree.xpath('//author/middle/text()')[0]

    def author_last(self):
        return self.tree.xpath('//author/last/text()')[0]

    def language(self):
        return self.tree.xpath('//language/text()')[0]

    def pub_date_start(self):
        raw = self.tree.xpath('//pubDate/pubDateStart/text()')[0]
        return int(raw[:4])

    def ocr(self):
        return float(self.tree.xpath('//ocr/text()')[0])

    def text(self):
        tokens = self.tree.xpath('//page[@type="bodyPage"]//wd/text()')
        return ' '.join(tokens)

    def row(self):
        """Assemble a DF row.

        Returns: GaleNovel
        """
        text = self.text()
        tokens = Token.parse(text)

        fields = dict(text=text, tokens=tokens)

        fields = {**fields, **{
            key: getattr(self, key)()
            for key in GaleNovel.schema.names
            if key not in fields
        }}

        return GaleNovel(**fields)
