

import re

from collections import Counter


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

    def token_pos_count(self):

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

            for pos, count in pos_count.items():
                counts[token, pos] += count

        return counts
