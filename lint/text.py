

import re

from collections import namedtuple, Counter

from nltk.tokenize import WordPunctTokenizer
from nltk import pos_tag

from textblob.utils import PUNCTUATION_REGEX

from lint.utils import clean_token, make_offset


Token = namedtuple('Token', [
    'token',
    'char1',
    'char2',
])


Tag = namedtuple('Tag', [
    'token',
    'char1',
    'char2',
    'pos',
])


class Text:

    def __init__(self, text: str):

        """
        Tokenize the text.
        """

        self.text = text

        tokenizer = WordPunctTokenizer()

        self.tokens = [

            Token(
                token=self.text[c1:c2],
                char1=c1,
                char2=c2,
            )

            for c1, c2 in tokenizer.span_tokenize(self.text)

        ]

    def pos_tags(self):

        """
        POS-tag the token stream.
        """

        tags = pos_tag([t.token for t in self.tokens])

        return [

            Tag(
                token=clean_token(t.token),
                char1=t.char1,
                char2=t.char2,
                pos=pos,
            )

            for (token, pos), t in zip(tags, self.tokens)
            if not PUNCTUATION_REGEX.match(token)

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

        # prefix start
        char1 = self.tokens[max(offset-padding, 0)].char1

        # token start
        char2 = self.tokens[offset].char1

        # suffix start
        char3 = self.tokens[offset].char2

        # suffix end
        char4 = self.tokens[min(offset+padding, len(self.tokens)-1)].char2

        return (
            self.text[char1:char2],
            self.text[char2:char3],
            self.text[char3:char4],
        )
