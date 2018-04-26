

import os
import ujson
import bz2
import random

from lxml import etree

from collections import OrderedDict

from . import fs
from .utils import read_csv, try_or_none

from .models import Text, GaleNovel, ChicagoNovel, ChicagoAuthor, \
    HathiToken, HathiVolume


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


class HathiVolumeJSON:

    @classmethod
    def read(cls, genre_row, vol_root):
        """Read JSON, patch in genre metadata.
        """
        path = os.path.join(vol_root, f'{genre_row.htid}.json.bz2')
        data = ujson.load(bz2.open(fs.read(path)))
        return cls(data, genre_row.genre, genre_row.p1, genre_row.p2)

    def __init__(self, data, genre_pred, p1, p2):
        self.data = data
        self.genre_pred = genre_pred
        self.p1 = p1
        self.p2 = p2

    def id(self):
        return self.data['id']

    def title(self):
        return self.data['metadata']['title']

    def names(self):
        return self.data['metadata']['names']

    def pub_date(self):
        return int(self.data['metadata']['pubDate'])

    def genre(self):
        return self.data['metadata']['genre']

    def language(self):
        return self.data['metadata']['language']

    def tokens(self):
        """Randomly splat page tokens to linear order.
        """
        tokens = []
        for page in self.data['features']['pages'][self.p1:self.p2+1]:

            page_tokens = []
            for token, pos_count in page['body']['tokenPosCount'].items():
                for pos, count in pos_count.items():
                    page_tokens += [HathiToken(token, pos)] * count

            random.shuffle(page_tokens)
            tokens += page_tokens

        return tokens

    def row(self):
        return HathiVolume(
            id=self.id(),
            title=self.title(),
            names=self.names(),
            pub_date=self.pub_date(),
            language=self.language(),
            genre_pred=self.genre_pred,
            tokens=self.tokens()
        )
