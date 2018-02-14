

import attr

from lxml import etree

from . import fs


@attr.s
class GaleNovelXML:

    tree = attr.ib()

    @classmethod
    def read(cls, path):
        return cls(etree.parse(fs.read(path)))

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

    def document_type(self):
        return self.tree.xpath('//documentType/text()')[0]

    def text(self):
        tokens = self.tree.xpath('//page[@type="bodyPage"]//wd/text()')
        return ' '.join(tokens)
