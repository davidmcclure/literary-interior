

import re
import spacy

from pyspark.sql import SparkSession, types as T
from collections import namedtuple

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
        T.StructField('text', T.StringType()),
        T.StructField('lemma', T.StringType()),
        T.StructField('pos', T.StringType()),
        T.StructField('tag', T.StringType()),
        T.StructField('dep', T.StringType()),

        # Position
        T.StructField('sent_i', T.IntegerType()),
        T.StructField('word_i', T.IntegerType()),
        T.StructField('char_i', T.IntegerType()),

    ])


class Text(Model):

    schema = T.StructType([
        T.StructField('raw', T.StringType()),
        T.StructField('tokens', T.ArrayType(Token.schema)),
    ])

    @classmethod
    def parse(cls, raw):
        """Parse a raw text string.

        Args:
            raw (str)

        Returns: list[Token]
        """
        tokens_iter = Tokenizer(raw)

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

        return cls(raw=raw, tokens=tokens)


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
        T.StructField('text', Text.schema),
    ])
