

import ujson

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    PrimaryKeyConstraint,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from lint.utils import scan_paths
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

    char1 = Column(Integer, nullable=False)

    char2 = Column(Integer, nullable=False)

    offset = Column(Integer, nullable=False)

    ratio = Column(Float, nullable=False)

    @classmethod
    def gather(cls, result_dir: str):

        """
        Bulk-insert tokens.
        """

        # Walk paths.
        for i, path in enumerate(scan_paths(result_dir)):
            with open(path) as fh:

                mappings = ujson.load(fh)

                # Bulk-insert rows.
                session.bulk_insert_mappings(cls, mappings)
                session.commit()

                print(i)

    def snippet(self, padding: int=500):

        """
        Get a snippet from the source text.
        """

        return self.text.snippet(
            self.char1,
            self.char2,
            padding,
        )
