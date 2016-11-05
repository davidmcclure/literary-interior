

import json

from scandir import scandir

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

from lint.singletons import session
from lint.models import Base


class Text(Base):

    __tablename__ = 'text'

    __table_args__ = (
        PrimaryKeyConstraint(
            'corpus',
            'identifier',
        ),
    )

    corpus = Column(String, nullable=False)

    identifier = Column(String, nullable=False)

    title = Column(String, nullable=False)

    author_first = Column(String, nullable=False)

    author_last = Column(String, nullable=False)

    year = Column(Integer, nullable=False)

    text = Column(String, nullable=False)

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

                data = json.load(fh)

                session.add(cls(**data))
                print(i)

        session.commit()
