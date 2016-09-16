

import pickle

from collections import OrderedDict
from scandir import scandir

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.sql import text, func

from lint.singletons import config, session
from lint.models import Base
from lint.utils import flatten_dict, mem_pct, grouper
from lint.offset_cache import OffsetCache


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

    # TODO: pos

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
        results = OffsetCache.from_results(result_dir)

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
            offsets (OffsetCache)
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
    def get(cls, corpus, token, year, offset):

        """
        Get a token count by the composite primary key.

        Args:
            corpus (str)
            token (str)
            year (int)
            offset (int)

        Returns: int
        """

        res = (
            session
            .query(cls.count)
            .filter_by(
                corpus=corpus,
                token=token,
                year=year,
                offset=offset,
            )
        )

        return res.scalar() or 0
