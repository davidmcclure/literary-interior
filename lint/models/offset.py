

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

        session.commit()

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

        cls.flush(offsets)

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
            .filter_by(
                token=token,
                year=year,
                offset=offset,
            )
        )

        return res.scalar() or 0

    @classmethod
    def baseline_series(cls, year1=None, year2=None):

        """
        Get an offset -> count series for a all words over a range of years.

        Args:
            year1 (int)
            year1 (int)

        Returns: OrderedDict
        """

        query = (
            session
            .query(cls.offset, func.sum(cls.count))
            .group_by(cls.offset)
            .order_by(cls.offset)
        )

        if year1:
            query = query.filter(cls.year >= year1)

        if year2:
            query = query.filter(cls.year <= year2)

        return OrderedDict(query.all())

    @classmethod
    def token_series(cls, token, year1=None, year2=None):

        """
        Get an offset -> count series for a word over a range of years.

        Args:
            token (str)
            year1 (int)
            year1 (int)

        Returns: OrderedDict
        """

        query = (
            session
            .query(cls.offset, func.sum(cls.count))
            .filter(cls.token==token)
            .group_by(cls.offset)
            .order_by(cls.offset)
        )

        if year1:
            query = query.filter(cls.year >= year1)

        if year2:
            query = query.filter(cls.year <= year2)

        return OrderedDict(query.all())

    @classmethod
    def token_counts(cls, year1=None, year2=None):

        """
        Get total token counts for all words over a range of years.

        Args:
            year1 (int)
            year1 (int)

        Returns: OrderedDict
        """

        query = (
            session
            .query(cls.token, func.sum(cls.count).label('count'))
            .group_by(cls.token)
            .order_by('count DESC')
        )

        if year1:
            query = query.filter(cls.year >= year1)

        if year2:
            query = query.filter(cls.year <= year2)

        return OrderedDict(query.all())
