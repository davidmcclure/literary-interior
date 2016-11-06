

import json

from scandir import scandir

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    PrimaryKeyConstraint,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from lint.singletons import session
from lint.models import Base


class Token(Base):

    __tablename__ = 'token'

    __table_args__ = (
        PrimaryKeyConstraint(
            'text_id',
            'token',
            'offset',
        ),
    )

    text_id = Column(Integer, ForeignKey('text.id'))

    text = relationship('Text')

    token = Column(String, nullable=False)

    pos = Column(String, nullable=False)

    offset = Column(Integer, nullable=False)

    ratio = Column(Integer, nullable=False)

    @classmethod
    def gather(cls, result_dir: str):

        """
        Bulk-insert tokens.
        """

        # Gather JSON paths.
        paths = [
            d.path
            for d in scandir(result_dir)
            if d.is_file()
        ]

        # Walk paths.
        for i, path in enumerate(paths):
            with open(path) as fh:

                mappings = json.load(fh)

                session.bulk_insert_mappings(cls, mappings)
                print(i)

        session.commit()
