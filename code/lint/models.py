

import re
import spacy

from pyspark.sql import SparkSession, types as T
from collections import namedtuple

from .sources import GaleNovelXML


nlp = spacy.load('en')


class ModelMeta(type):

    def __new__(meta, name, bases, dct):
        """Generate a namedtuple from the `schema` class attribute.
        """
        if isinstance(dct.get('schema'), T.StructType):

            Row = namedtuple(name, dct['schema'].names)

            # By default, default all fields to None.
            Row.__new__.__defaults__ = (None,) * len(Row._fields)

            bases = (Row,) + bases

        return super().__new__(meta, name, bases, dct)


class Model(metaclass=ModelMeta):

    @classmethod
    def from_rdd(cls, row):
        """Wrap a raw `Row` instance from an RDD as a model instance.

        Args:
            row (pyspark.sql.Row)

        Returns: Model
        """
        return cls(**row.asDict())


class Token(Model):

    schema = T.StructType([

        # Token
        T.StructField('text', T.StringType()),
        T.StructField('lemma', T.StringType()),
        T.StructField('pos', T.StringType()),
        T.StructField('tag', T.StringType()),
        T.StructField('dep', T.StringType()),

        # Position
        T.StructField('word_i', T.IntegerType()),
        T.StructField('char_i', T.IntegerType()),
        T.StructField('offset', T.FloatType()),

    ])

    @classmethod
    def parse(cls, text):
        """Parse a raw text string.

        Args:
            text (str)

        Returns: list[Token]
        """
        doc = nlp(text)

        return [
            cls(
                text=t.text,
                lemma=t.lemma_,
                pos=t.pos_,
                tag=t.tag_,
                dep=t.dep_,
                word_i=t.i,
                char_i=t.idx,
                offset=(t.i / (len(doc)-1))
            )
            for t in doc
        ]


class GaleNovel(Model):

    schema = T.StructType([
        T.StructField('psmid', T.StringType()),
        T.StructField('full_title', T.StringType()),
        T.StructField('author_first', T.StringType()),
        T.StructField('author_middle', T.StringType()),
        T.StructField('author_last', T.StringType()),
        T.StructField('language', T.StringType()),
        T.StructField('pub_date_start', T.IntegerType()),
        T.StructField('ocr', T.FloatType()),
        T.StructField('text', T.StringType()),
        T.StructField('tokens', T.ArrayType(Token.schema)),
    ])

    @classmethod
    def from_xml(cls, path):
        """Make row from XML source.
        """
        xml = GaleNovelXML.read(path)

        fields = {
            name: getattr(xml, name)()
            for name in cls.schema.names
            if hasattr(xml, name)
        }

        fields['tokens'] = Token.parse(fields['text'])

        return cls(**fields)


class ChicagoNovel(Model):

    schema = T.StructType([
        T.StructField('book_id', T.StringType()),
        T.StructField('filename', T.StringType()),
        T.StructField('libraries', T.IntegerType()),
        T.StructField('title', T.StringType()),
        T.StructField('auth_last', T.StringType()),
        T.StructField('auth_first', T.StringType()),
        T.StructField('auth_id', T.StringType()),
        T.StructField('publ_city', T.StringType()),
        T.StructField('publisher', T.StringType()),
        T.StructField('publ_date', T.IntegerType()),
        T.StructField('source', T.StringType()),
        T.StructField('nationality', T.StringType()),
        T.StructField('genre', T.StringType()),
        T.StructField('clean', T.BooleanType()),
        T.StructField('text', T.StringType()),
        T.StructField('tokens', T.ArrayType(Token.schema)),
    ])


class Novel(Model):

    schema = T.StructType([
        T.StructField('corpus', T.StringType()),
        T.StructField('identifier', T.StringType()),
        T.StructField('title', T.StringType()),
        T.StructField('author_first', T.StringType()),
        T.StructField('author_last', T.StringType()),
        T.StructField('year', T.IntegerType()),
        T.StructField('text', T.StringType()),
        T.StructField('tokens', T.ArrayType(Token.schema)),
    ])
