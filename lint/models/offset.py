

import scandir
import pickle

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.sql import text

from clint.textui import progress

from lint import config
from lint.models import BaseModel


class Offset(BaseModel):


    __tablename__ = 'count'

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

        session = config.Session()

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

        session.commit()


    @classmethod
    def gather_results(cls, root):

        """
        Given a directory of pickled count caches, unpickle the caches and
        emrge the counts into the database.

        Args:
            root (str)
        """

        paths = [
            d.path
            for d in scandir.scandir(root)
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

        with config.get_session() as session:

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
