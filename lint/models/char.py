

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

from lint.singletons import session
from lint.models import Base
from lint.count_cache import CountCache
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
    def gather_results(cls, corpus, result_dir):

        """
        Merge and insert pickled count caches.

        Args:
            corpus (str)
            result_dir (str)
        """

        # Merge result pickles.
        results = CountCache.from_results(result_dir)

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

    # TODO: Don't duplicate this?

    @classmethod
    def delete_corpus(cls, corpus):

        """
        Clear all counts for a corpus.

        Args:
            corpus (str)
        """

        cls.query.filter_by(corpus=corpus).delete()

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
