

import os
import ujson
import bz2
import random

from lxml import etree

from collections import OrderedDict

from . import fs
from .models import Text, GaleNovel, ChicagoNovel, ChicagoAuthor
from .utils import read_csv, try_or_none


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
        return round(float(self.tree.findtext('//ocr')))

    def raw_text(self):
        tokens = self.tree.findall('//page[@type="bodyPage"]//wd')
        return ' '.join([t.text for t in tokens if t.text])

    def text(self):
        return Text.parse(self.raw_text())

    def row(self):
        return GaleNovel(**{
            name: getattr(self, name)()
            for name in GaleNovel.schema.names
        })


class CSVRow(OrderedDict):

    def __getitem__(self, key):
        """Cast empty CSV values '' -> None.
        """
        val = super().__getitem__(key)
        return val if val != '' else None


class ChicagoNovelCSVRow(CSVRow):

    def __init__(self, fields, text_dir):
        super().__init__(fields)
        self.text_dir = text_dir

    def book_id(self):
        return int(self['BOOK_ID'])

    def filename(self):
        return self['FILENAME']

    def libraries(self):
        return int(self['LIBRARIES'])

    def title(self):
        return self['TITLE']

    def auth_last(self):
        return self['AUTH_LAST']

    def auth_first(self):
        return self['AUTH_FIRST']

    def auth_id(self):
        return self['AUTH_ID']

    def publ_city(self):
        return self['PUBL_CITY']

    def publisher(self):
        return self['PUBLISHER']

    def publ_date(self):
        return int(self['PUBL_DATE'])

    def source(self):
        return self['SOURCE']

    def nationality(self):
        return self['NATIONALITY']

    def genre(self):
        return self['GENRE']

    def clean(self):
        return self['CLEAN?'] == 'c'

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


class ChicagoAuthorCSVRow(CSVRow):

    @classmethod
    def read_csv(cls, path):
        for fields in read_csv(path):
            yield cls(fields).row()

    def auth_id(self):
        return self['AUTH_ID']

    def auth_last(self):
        return self['AUTH_LAST']

    def auth_first(self):
        return self['AUTH_FIRST']

    def canon(self):
        return self['CANON'] == 'C'

    @try_or_none
    def date_b(self):
        return int(self['DATE_B'])

    @try_or_none
    def date_d(self):
        return int(self['DATE_D'])

    def nationality(self):
        return self['NATIONALITY']

    def gender(self):
        return self['GENDER']

    def race(self):
        return self['RACE']

    def hyphenated_identity(self):
        return self['HYPHENATED_IDENTITY']

    @try_or_none
    def immigrant(self):
        return int(self['IMMIGRANT'])

    def sexual_identity(self):
        return self['SEXUAL_IDENTITY']

    def education(self):
        return self['EDUCATION']

    def mfa(self):
        return self['MFA']

    def secondary_occupation(self):
        return self['SECONDARY_OCCUPATION']

    def coterie(self):
        return self['COTERIE']

    def religion(self):
        return self['RELIGION']

    def ses(self):
        return self['CLASS']

    def geography(self):
        return self['GEOGRAPHY']

    def row(self):
        return ChicagoAuthor(**{
            name: getattr(self, name)()
            for name in ChicagoAuthor.schema.names
        })
