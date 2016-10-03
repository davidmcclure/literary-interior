

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

from lint.singletons import session
from lint.models import Base
from lint.utils import grouper


class Char(Base):


    __tablename__ = 'char'

    __table_args__ = (
        PrimaryKeyConstraint(
            'corpus',
            'year',
            'char',
            'offset',
        ),
    )

    corpus = Column(String, nullable=False)

    year = Column(Integer, nullable=False)

    char = Column(String, nullable=False)

    offset = Column(Integer, nullable=False)

    count = Column(Integer, nullable=False)


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
                    char=char,
                    offset=offset,
                    count=count,
                )
                for (year, char, offset), count in group
            ]

            session.bulk_insert_mappings(cls, mappings)

    @classmethod
    def get(cls, corpus, year, char, offset):

        """
        Get a char count by the composite primary key.

        Args:
            corpus (str)
            year (int)
            char (str)
            offset (int)

        Returns: int
        """

        res = (
            session
            .query(cls.count)
            .filter_by(
                corpus=corpus,
                year=year,
                char=char,
                offset=offset,
            )
        )

        return res.scalar() or 0
