

import json

from collections import namedtuple
from scandir import scandir

from sqlalchemy import Column, Integer, String, UniqueConstraint
from nltk.tokenize import WordPunctTokenizer

from lint.singletons import session
from lint.models import Base


Token = namedtuple('Token', [
    'token',
    'char1',
    'char2',
])


class Text(Base):

    __tablename__ = 'text'

    __table_args__ = (
        UniqueConstraint(
            'corpus',
            'identifier',
        ),
    )

    id = Column(Integer, primary_key=True)

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

    def tokens(self):

        """
        Tokenize the text.
        """

        tokenizer = WordPunctTokenizer()

        spans = tokenizer.span_tokenize(self.text)

        return [

            Token(
                token=self.text[c1:c2],
                char1=c1,
                char2=c2,
            )

            for i, (c1, c2) in enumerate(spans)

        ]
