

import re

from collections import namedtuple

from nltk.tokenize import WordPunctTokenizer
from nltk import pos_tag


Token = namedtuple('Token', [
    'token',
    'char1',
    'char2',
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
