

import re

from collections import Counter

from lint.singletons import tokens


class Page:

    def __init__(self, data):

        """
        Wrap an individual page.

        Args:
            data (dict)
        """

        self.data = data

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
        for token, pos_count in self.data['body']['tokenPosCount'].items():

            token = token.lower()

            # Ignore irregular tokens.
            if not letters.match(token):
                continue

            # Apply token whitelist.
            if token not in tokens:
                continue

            counts[token] += sum(pos_count.values())

        return counts
