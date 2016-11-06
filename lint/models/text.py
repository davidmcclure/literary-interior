

import ujson

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
    'offset',
    'ratio',
])


TaggedToken = namedtuple('Tag',
    Token._fields +
    ('pos',)
)


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

                data = ujson.load(fh)

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

        spans = list(tokenizer.span_tokenize(self.text))

        return [

            Token(

                token=self.text[c1:c2],

                char1=c1,
                char2=c2,

                # TODO: Move to job?

                offset=i,
                ratio=i/len(spans)

            )

            for i, (c1, c2) in enumerate(spans)

        ]

    def tagged_tokens(self):

        """
        POS-tag the token stream.
        """

        tokens = self.tokens()

        tags = pos_tag([t.token for t in tokens])

        return [

            # TODO: Mass-assign the token?

            TaggedToken(

                token=token.token.lower(),

                char1=token.char1,
                char2=token.char2,

                offset=token.offset,
                ratio=token.ratio,

                pos=pos,

            )

            for token, (_, pos) in zip(tokens, tags)

        ]

    def bucket_counts(self, bins: int):

        """
        Map (token, POS, offset) -> count.

        Returns: Counter
        """

        tags = self.tagged_tokens()

        counts = Counter()

        for i, tag in enumerate(tags):

            # Make 0-N offset.
            offset = make_offset(i, len(tags), bins)

            counts[tag.token, tag.pos, offset] += 1

        return counts

    def snippet(self, char1: int, char2: int, padding: int=500):

        """
        Hydrate a snippet.

        Returns: (prefix, token, suffix)
        """

        char0 = max(char1-padding, 0)
        char3 = min(char2+padding, len(self.text))

        return (
            self.text[char0:char1],
            self.text[char1:char2],
            self.text[char2:char3],
        )
