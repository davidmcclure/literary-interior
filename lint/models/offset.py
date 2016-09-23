

import pickle

from collections import OrderedDict
from scandir import scandir

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.sql import text, func

from lint.singletons import config, session
from lint.models import Base
from lint.utils import flatten_dict, mem_pct, grouper
from lint.count_cache import CountCache


# TODO: Rename to Count?


class Offset(Base):


    __tablename__ = 'offset'

    __table_args__ = (
        PrimaryKeyConstraint(
            'corpus',
            'year',
            'token',
            'pos',
            'offset',
        ),
    )

    corpus = Column(String, nullable=False)

    year = Column(Integer, nullable=False)

    token = Column(String, nullable=False)

    pos = Column(String, nullable=False)

    offset = Column(Integer, nullable=False)

    count = Column(Integer, nullable=False)


    @classmethod
    def gather_results(cls, corpus, result_dir):

        """
        Merge and insert pickled count caches.

        Args:
            corpus (str)
            result_dir (str)
        """

        # Merge result pickles.
        results = CountCache.from_results(result_dir)

        # Clear and insert the counts.
        cls.delete_corpus(corpus)
        cls.insert_corpus(corpus, results)

        session.commit()

    @classmethod
    def insert_corpus(cls, corpus, offsets):

        """
        Flush an offset cache to disk.

        Args:
            corpus (str)
            offsets (CountCache)
        """

        for group in grouper(offsets.flatten(), 1000):

            mappings = [
                dict(
                    corpus=corpus,
                    year=year,
                    token=token,
                    pos=pos,
                    offset=offset,
                    count=count,
                )
                for (year, token, pos, offset), count in group
            ]

            session.bulk_insert_mappings(cls, mappings)

    @classmethod
    def delete_corpus(cls, corpus):

        """
        Clear all counts for a corpus.

        Args:
            corpus (str)
        """

        cls.query.filter_by(corpus=corpus).delete()

    @classmethod
    def get(cls, corpus, year, token, pos, offset):

        """
        Get a token count by the composite primary key.

        Args:
            corpus (str)
            year (int)
            token (str)
            pos (str)
            offset (int)

        Returns: int
        """

        res = (
            session
            .query(cls.count)
            .filter_by(
                corpus=corpus,
                year=year,
                token=token,
                pos=pos,
                offset=offset,
            )
        )

        return res.scalar() or 0

    @classmethod
    def baseline_series(cls, corpus=None):

        """
        Get an offset -> count series.

        Args:
            corpus (str)

        Returns: OrderedDict
        """

        query = (
            session
            .query(cls.offset, func.sum(cls.count))
            .group_by(cls.offset)
            .order_by(cls.offset)
        )

        if corpus:
            query = query.filter(cls.corpus==corpus)

        return OrderedDict(query.all())

    @classmethod
    def token_series(cls, token, corpus=None):

        """
        Get an offset -> count series for a word.

        Args:
            token (str)
            corpus (str)

        Returns: OrderedDict
        """

        query = (
            session
            .query(cls.offset, func.sum(cls.count))
            .filter(cls.token==token)
            .group_by(cls.offset)
            .order_by(cls.offset)
        )

        if corpus:
            query = query.filter(cls.corpus==corpus)

        return OrderedDict(query.all())

    @classmethod
    def pos_series(cls, pos, corpus=None):

        """
        Get an offset -> count series for a POS.

        Args:
            pos (str)
            corpus (str)

        Returns: OrderedDict
        """

        query = (
            session
            .query(cls.offset, func.sum(cls.count))
            .filter(cls.pos==pos)
            .group_by(cls.offset)
            .order_by(cls.offset)
        )

        if corpus:
            query = query.filter(cls.corpus==corpus)

        return OrderedDict(query.all())
