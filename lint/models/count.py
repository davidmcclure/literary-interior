

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

from lint import config
from lint.models import BaseModel


class Count(BaseModel):


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
            cache (CountCache)
        """

        pass


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
