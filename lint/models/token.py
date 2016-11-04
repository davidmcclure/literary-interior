

import pickle

from scandir import scandir

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    PrimaryKeyConstraint,
)

from lint.singletons import session
from lint.models import Base


class Token(Base):

    __tablename__ = 'token'

    __table_args__ = (
        PrimaryKeyConstraint(
            'corpus',
            'identifier',
            'offset',
        ),
    )

    corpus = Column(String, nullable=False)

    identifier = Column(String, nullable=False)

    year = Column(Integer, nullable=False)

    token = Column(String, nullable=False)

    pos = Column(String, nullable=False)

    offset = Column(Integer, nullable=False)

    ratio = Column(Float, nullable=False)

    @classmethod
    def gather(cls, result_dir: str):

        """
        Bulk-insert tokens.
        """

        # Gather pickle paths.
        paths = [
            d.path
            for d in scandir(result_dir)
            if d.is_file()
        ]

        # Walk paths.
        for i, path in enumerate(paths):
            with open(path, 'rb') as fh:

                mappings = pickle.load(fh)

                # Bulk-insert the rows.
                session.bulk_insert_mappings(cls, mappings)
                print(i)

        session.commit()

    @classmethod
    def exists(cls, **kwargs):

        """
        Check that a row exists.
        """

        return cls.query.filter_by(**kwargs).count() == 1
