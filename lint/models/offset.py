

import pickle

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.sql import text

from scandir import scandir
from clint.textui import progress

from lint.singletons import config, session
from lint.models import Base
from lint.utils import flatten_dict, mem_pct, grouper
from lint.offset_cache import OffsetCache


class Offset(Base):


    __tablename__ = 'offset'

    __table_args__ = (
        PrimaryKeyConstraint('token', 'year', 'offset'),
    )

    token = Column(String, nullable=False)

    year = Column(Integer, nullable=False)

    offset = Column(Integer, nullable=False)

    count = Column(Integer, nullable=False)


    @classmethod
    def flush(cls, cache):

        """
        Flush an offset cache to disk.

        Args:
            cache (OffsetCache)
        """

        for group in grouper(flatten_dict(cache), 1000):

            mappings = [
                dict(
                    token=token,
                    year=year,
                    offset=offset,
                    count=count,
                )
                for year, token, offset, count in group
            ]

            session.bulk_insert_mappings(cls, mappings)

    @classmethod
    def gather_results(cls, result_dir):

        """
        Unpickle the offset caches and merge the counts.

        Args:
            result_dir (str)
        """

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

        # Write to disk.
        cls.flush(offsets)

        session.commit()

    @classmethod
    def token_year_offset_count(cls, token, year, offset):

        """
        How many times did token X appear in year Y as offset Z?

        Args:
            token (str)
            year (int)
            offset (int)

        Returns: int
        """

        res = (
            session
            .query(cls.count)
            .filter(
                cls.token==token,
                cls.year==year,
                cls.offset==offset,
            )
        )

        return res.scalar() or 0
