

import re

from collections import Counter

from lint import config


class Page:

    def __init__(self, data):

        """
        Wrap an individual page.

        Args:
            data (dict)
        """

        self.data = data

    @property
    def token_count(self):

        """
        Get the total token count on the page.

        Returns: int
        """

        return int(self.data['body']['tokenCount'])

    def merged_token_counts(self):

        """
        Count the total occurrences of each unique token.

        Returns: Counter
        """

        # Match letters.
        letters = re.compile('^[a-z]+$')

        counts = Counter()
        for token, pc in self.data['body']['tokenPosCount'].items():

            token = token.lower()

            # Ignore irregular tokens.
            if not letters.match(token):
                continue

            # Apply token whitelist.
            if token not in config.tokens:
                continue

            counts[token] += sum(pc.values())

        return counts
