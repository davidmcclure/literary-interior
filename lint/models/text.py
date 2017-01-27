

import ujson

from collections import namedtuple, Counter
from scandir import scandir

from sqlalchemy import Column, Integer, String, UniqueConstraint
from nltk import pos_tag
from nltk.tokenize import WordPunctTokenizer

from lint.singletons import session
from lint.models import Base
from lint.utils import scan_paths, make_offset


Token = namedtuple('Token', [
    'token',
    'char1',
    'char2',
    'pos',
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

    title = Column(String, nullable=True)

    author_first = Column(String, nullable=True)

    author_last = Column(String, nullable=True)

    year = Column(Integer, nullable=False)

    text = Column(String, nullable=False)

    @classmethod
    def gather(cls, result_dir: str):
        """Bulk-insert tokens.
        """
        # Walk paths.
        for i, path in enumerate(scan_paths(result_dir)):
            with open(path) as fh:

                # Parse JSON.
                data = ujson.load(fh)

                # Insert row.
                session.add(cls(**data))
                session.commit()

                print(i)

    @classmethod
    def ids(cls):
        """Query a list of all ids.
        """
        query = session.query(cls.id).all()

        return [row[0] for row in query]

    def tokens(self):
        """Tokenize the text.
        """
        tokenizer = WordPunctTokenizer()

        # Get token character spans.
        spans = list(tokenizer.span_tokenize(self.text))

        # Materialize the token stream.
        tokens = [self.text[c1:c2] for c1, c2 in spans]

        tags = pos_tag(tokens)

        return [

            Token(
                token=token.lower(),
                char1=c1,
                char2=c2,
                pos=pos,
            )

            for (c1, c2), token, (_, pos) in
            zip(spans, tokens, tags)

        ]

    def bucket_counts(self, bins: int):
        """Map (token, POS, offset) -> count.

        Returns: Counter
        """
        tokens = self.tokens()

        counts = Counter()

        for i, token in enumerate(tokens):

            # Make 0-N offset.
            offset = make_offset(i, len(tokens), bins)

            # Increment the path.
            counts[token.token, token.pos, offset] += 1

        return counts

    def snippet(self, char1: int, char2: int, padding: int=500):
        """Hydrate a snippet.

        Returns: (prefix, token, suffix)
        """
        char0 = max(char1-padding, 0)
        char3 = min(char2+padding, len(self.text))

        return (
            self.text[char0:char1],
            self.text[char1:char2],
            self.text[char2:char3],
        )
