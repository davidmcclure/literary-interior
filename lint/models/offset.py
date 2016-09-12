

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
        PrimaryKeyConstraint('corpus', 'token', 'year', 'offset'),
    )

    # TODO: POS

    corpus = Column(String, nullable=False)

    token = Column(String, nullable=False)

    year = Column(Integer, nullable=False)

    offset = Column(Integer, nullable=False)

    count = Column(Integer, nullable=False)


    @classmethod
    def flush(cls, corpus, cache):

        """
        Flush an offset cache to disk.

        Args:
            corpus (str)
            cache (OffsetCache)
        """

        for group in grouper(flatten_dict(cache), 1000):

            mappings = [
                dict(
                    corpus=corpus,
                    token=token,
                    year=year,
                    offset=offset,
                    count=count,
                )
                for year, token, offset, count in group
            ]

            session.bulk_insert_mappings(cls, mappings)

        session.commit()

    @classmethod
    def gather_results(cls, result_dir):

        """
        Unpickle the offset caches and merge the counts.

        Args:
            result_dir (str)
        """

        # TODO: 'corpus' arg, clear existing rows for corpus.

        offsets = OffsetCache()

        # Gather pickled offset paths.
        paths = [
            d.path
            for d in scandir(result_dir)
            if d.is_file()
        ]

        # Walk paths.
        for i, path in enumerate(paths):
            with open(path, 'rb') as fh:

                # Merge offsets.
                offsets += pickle.load(fh)
                print(i, mem_pct())

        cls.flush(offsets)

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
