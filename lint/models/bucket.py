

import numpy as np

from collections import OrderedDict

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.sql import func

from lint.singletons import session
from lint.models import Base
from lint.count_cache import CountCache
from lint.utils import grouper


class Bucket(Base):

    __tablename__ = 'bucket'

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
    def gather(cls, result_dir):
        """Merge + insert pickled count caches.

        Args:
            result_dir (str)
        """
        # Merge result pickles.
        results = CountCache.from_results(result_dir)

        for group in grouper(results.flatten(), 1000):

            mappings = [
                dict(
                    corpus=corpus,
                    year=year,
                    token=token,
                    pos=pos,
                    offset=offset,
                    count=count,
                )
                for (
                    corpus,
                    year,
                    token,
                    pos,
                    offset,
                ), count in group
            ]

            session.bulk_insert_mappings(cls, mappings)

        session.commit()

    @classmethod
    def get(cls, corpus, year, token, pos, offset):
        """Get a token count by the composite primary key.

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
    def token_counts(cls, min_count=0):
        """Get total (un-bucketed) token counts.

        Args:
            min_count (int)

        Returns: OrderedDict
        """
        query = (
            session
            .query(cls.token, func.sum(cls.count))
            .group_by(cls.token)
            .having(func.sum(cls.count) > min_count)
            .order_by(func.sum(cls.count).desc())
        )

        return OrderedDict(query.all())

    @classmethod
    def token_series(cls, token, corpus=None, year1=None, year2=None):
        """Get an offset -> count series for a word.

        Args:
            token (str)
            corpus (str)

        Returns: OrderedDict
        """
        query = (
            session
            .query(cls.offset, func.sum(cls.count))
            .filter(cls.token == token)
            .group_by(cls.offset)
            .order_by(cls.offset)
        )

        if corpus:
            query = query.filter(cls.corpus == corpus)

        if year1:
            query = query.filter(cls.year >= year1)

        if year2:
            query = query.filter(cls.year <= year2)

        series = np.zeros(100)

        for offset, count in query:
            series[offset] = count

        return series
