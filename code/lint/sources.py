

from lxml import etree

from . import fs
from .utils import safe_cached_property
from .models import Text, GaleNovel


class GaleNovelXML:

    @classmethod
    def read(cls, path):
        return cls(etree.parse(fs.read(path)))

    def __init__(self, tree):
        self.tree = tree

    @safe_cached_property
    def psmid(self):
        return self.tree.find('//PSMID').text

    @safe_cached_property
    def full_title(self):
        return self.tree.find('//fullTitle').text

    @safe_cached_property
    def author_first(self):
        return self.tree.find('//author/first').text

    @safe_cached_property
    def author_middle(self):
        return self.tree.find('//author/middle').text

    @safe_cached_property
    def author_last(self):
        return self.tree.find('//author/last').text

    @safe_cached_property
    def language(self):
        return self.tree.find('//language').text

    @safe_cached_property
    def pub_date_start(self):
        raw = self.tree.find('//pubDate/pubDateStart').text
        return int(raw[:4])

    @safe_cached_property
    def ocr(self):
        return float(self.tree.find('//ocr').text)

    @safe_cached_property
    def raw_text(self):
        tokens = self.tree.findall('//page[@type="bodyPage"]//wd')
        return ' '.join([t.text for t in tokens])

    @safe_cached_property
    def text(self):
        return Text.parse(self.raw_text)

    def row(self):
        """Assemble a DF row.

        Returns: GaleNovel
        """
        return GaleNovel(**{
            name: getattr(self, name)
            for name in GaleNovel.schema.names
        })


class ChicagoNovelMetadata:

    def __init__(self, row, text_root):
        pass
