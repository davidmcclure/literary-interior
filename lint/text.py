

import re

from collections import namedtuple

from nltk.tokenize import WordPunctTokenizer
from nltk import pos_tag

from textblob.utils import PUNCTUATION_REGEX


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
            Tag(*t, pos)
            for (token, pos), t in zip(tags, self.tokens)
            if not PUNCTUATION_REGEX.match(token)
        ]
