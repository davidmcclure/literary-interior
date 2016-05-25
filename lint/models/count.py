

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

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
