

import os

from lxml import etree

from . import fs
from .models import Text, GaleNovel, ChicagoNovel
from .utils import safe_cached_property


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
        return ' '.join([t.text for t in tokens if t.text])

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

    def __init__(self, fields, text_dir):
        self.fields = fields
        self.text_dir = text_dir

    def book_id(self):
        return int(self.fields['BOOK_ID'])

    def filename(self):
        return self.fields['FILENAME']

    def libraries(self):
        return int(self.fields['LIBRARIES'])

    def title(self):
        return self.fields['TITLE']

    def auth_last(self):
        return self.fields['AUTH_LAST']

    def auth_first(self):
        return self.fields['AUTH_FIRST']

    def auth_id(self):
        return self.fields['AUTH_ID']

    def publ_city(self):
        return self.fields['PUBL_CITY']

    def publisher(self):
        return self.fields['PUBLISHER']

    def publ_date(self):
        return int(self.fields['PUBL_DATE'])

    def source(self):
        return self.fields['SOURCE']

    def nationality(self):
        return self.fields['NATIONALITY']

    def genre(self):
        return self.fields['GENRE']

    def clean(self):
        return self.fields['CLEAN?'] == 'c'

    def raw_text(self):
        fh = fs.read(os.path.join(self.text_dir, self.filename))
        return fh.read().decode()

    def text(self):
        return Text.parse(self.raw_text())

    def row(self):
        """Assemble a DF row.

        Returns: ChicagoNovel
        """
        return ChicagoNovel(**{
            name: getattr(self, name)()
            for name in ChicagoNovel.schema.names
        })
