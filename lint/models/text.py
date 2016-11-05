

import json

from collections import namedtuple, Counter
from scandir import scandir

from sqlalchemy import Column, Integer, String, UniqueConstraint
from nltk import pos_tag
from nltk.tokenize import WordPunctTokenizer

from lint.singletons import session
from lint.models import Base
from lint.utils import make_offset


Token = namedtuple('Token', [
    'token',
    'char1',
    'char2',
])


Tag = namedtuple('Tag', [
    'token',
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

    @classmethod
    def ids(cls):

        """
        Query a list of all ids.
        """

        query = session.query(cls.id).all()

        return [row[0] for row in query]

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

    def pos_tags(self):

        """
        POS-tag the token stream.
        """

        tags = pos_tag([t.token for t in self.tokens()])

        return [

            Tag(
                token=token.lower(),
                pos=pos,
            )

            for token, pos in tags

        ]

    def token_offset_counts(self, bins: int):

        """
        Map (token, POS, offset) -> count.

        Returns: Counter
        """

        tags = self.pos_tags()

        counts = Counter()

        for i, tag in enumerate(tags):

            # Make 0-N offset.
            offset = make_offset(i, len(tags), bins)

            counts[tag.token, tag.pos, offset] += 1

        return counts

    def snippet(self, offset: int, padding: int=10):

        """
        Hydrate a snippet.

        Returns: (prefix, token, suffix)
        """

        tokens = self.tokens()

        # prefix start
        char1 = tokens[max(offset-padding, 0)].char1

        # token start
        char2 = tokens[offset].char1

        # suffix start
        char3 = tokens[offset].char2

        # suffix end
        char4 = tokens[min(offset+padding, len(tokens)-1)].char2

        return (
            self.text[char1:char2],
            self.text[char2:char3],
            self.text[char3:char4],
        )
