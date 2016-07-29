

import pickle

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.sql import text

from scandir import scandir
from clint.textui import progress

from lint.singletons import config, session
from lint.models import Base


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
    def increment(cls, cache):

        """
        Given a count cache, increment the counters in the database.

        Args:
            cache (OffsetCache)
        """

        # SQLite "upsert."
        query = text("""

            INSERT OR REPLACE INTO {table!s} (
                token,
                year,
                offset,
                count
            )

            VALUES (
                :token,
                :year,
                :offset,
                :count + COALESCE(
                    (
                        SELECT count FROM {table!s} WHERE (
                            token = :token AND
                            year = :year AND
                            offset = :offset
                        )
                    ),
                    0
                )
            )

        """.format(table=cls.__tablename__))

        for year, token, offset, count in cache.flatten():

            session.execute(query, dict(
                token=token,
                year=year,
                offset=offset,
                count=count,
            ))

    @classmethod
    def gather_results(cls, result_dir):

        """
        Unpickle the offset caches and merge the counts.

        Args:
            result_dir (str)
        """

        # TODO: Merge all in memory, flush once.

        paths = [
            d.path
            for d in scandir(result_dir)
            if d.is_file()
        ]

        for path in progress.bar(paths):
            with open(path, 'rb') as fh:
                cls.increment(pickle.load(fh))

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
