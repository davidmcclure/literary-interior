

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

    def psmid(self):
        return self.tree.findtext('//PSMID')

    def full_title(self):
        return self.tree.findtext('//fullTitle')

    def author_first(self):
        return self.tree.findtext('//author/first')

    def author_middle(self):
        return self.tree.findtext('//author/middle')

    def author_last(self):
        return self.tree.findtext('//author/last')

    def language(self):
        return self.tree.findtext('//language')

    def pub_date_start(self):
        raw = self.tree.findtext('//pubDate/pubDateStart')
        return int(raw[:4])

    def ocr(self):
        return float(self.tree.findtext('//ocr'))

    def raw_text(self):
        tokens = self.tree.findall('//page[@type="bodyPage"]//wd')
        return ' '.join([t.text for t in tokens if t.text])

    def text(self):
        return Text.parse(self.raw_text)

    def row(self):
        return GaleNovel(**{
            name: getattr(self, name)()
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
        fh = fs.read(os.path.join(self.text_dir, self.filename()))
        return fh.read().decode()

    def text(self):
        return Text.parse(self.raw_text())

    def row(self):
        return ChicagoNovel(**{
            name: getattr(self, name)()
            for name in ChicagoNovel.schema.names
        })
