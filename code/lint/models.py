

import re
import spacy

from pyspark.sql import SparkSession, types as T
from collections import namedtuple

from .utils import clean_text
from .tokenizer import Tokenizer


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
        T.StructField('text', T.StringType(), nullable=False),
        T.StructField('lemma', T.StringType(), nullable=False),
        T.StructField('pos', T.StringType(), nullable=False),
        T.StructField('tag', T.StringType(), nullable=False),
        T.StructField('dep', T.StringType(), nullable=False),

        # Position
        T.StructField('sent_i', T.IntegerType(), nullable=False),
        T.StructField('word_i', T.IntegerType(), nullable=False),
        T.StructField('char_i', T.IntegerType(), nullable=False),

    ])


class Text(Model):

    schema = T.StructType([
        T.StructField('raw', T.StringType(), nullable=False),
        T.StructField('tokens', T.ArrayType(Token.schema), nullable=False),
    ])

    @classmethod
    def parse(cls, raw):
        """Parse a raw text string.

        Args:
            raw (str)

        Returns: list[Token]
        """
        clean = clean_text(raw)

        tokens_iter = Tokenizer(clean)

        # TODO: Save parse head pointers.
        tokens = [
            Token(
                text=t.text,
                lemma=t.lemma_,
                pos=t.pos_,
                tag=t.tag_,
                dep=t.dep_,
                sent_i=sent_i,
                word_i=word_i,
                char_i=char_i,
            )
            for t, sent_i, word_i, char_i in tokens_iter
        ]

        return cls(raw=clean, tokens=tokens)


class GaleNovel(Model):

    schema = T.StructType([
        T.StructField('psmid', T.StringType(), nullable=False),
        T.StructField('full_title', T.StringType()),
        T.StructField('author_first', T.StringType()),
        T.StructField('author_middle', T.StringType()),
        T.StructField('author_last', T.StringType()),
        T.StructField('language', T.StringType()),
        T.StructField('pub_date_start', T.IntegerType()),
        T.StructField('ocr', T.IntegerType()),
        T.StructField('text', Text.schema, nullable=False),
    ])


class ChicagoNovel(Model):

    schema = T.StructType([
        T.StructField('book_id', T.IntegerType(), nullable=False),
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
        T.StructField('text', Text.schema, nullable=False),
    ])
