

import os
import re

from cached_property import cached_property


class Text:


    @classmethod
    def from_file(cls, path):

        """
        Create a text from a file.

        Args:
            path (str)
        """

        with open(path, 'r', errors='replace') as f:
            return cls(f.read())


    def __init__(self, text):

        """
        Set the raw text.

        Args:
            text (str)
        """

        self.text = text

        self.tokenize()


    def tokenize(self):

        """
        Tokenize the text.
        """

        self.tokens  = []
        self.offsets = {}

        pattern = re.finditer('[a-z]+', self.text.lower())

        for offset, match in enumerate(pattern):

            token = match.group(0)

            # Store token.
            self.tokens.append(token)

            # Store integer offset.
            offsets = self.offsets.setdefault(token, [])
            offsets.append(offset)


    @cached_property
    def ratios(self):

        """
        Get term -> [0-1 ratios]

        Returns: dict
        """

        ratios = {}

        for token, offsets in self.offsets.items():
            ratios[token] = [i / (len(self.tokens)-1) for i in offsets]

        return ratios
