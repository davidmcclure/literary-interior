

import json
import bz2

from collections import defaultdict, Counter

from lint.htrc.page import Page


class Volume:

    @classmethod
    def from_path(cls, path):

        """
        Inflate a volume and make an instance.

        Args:
            path (str)

        Returns: cls
        """

        with bz2.open(path, 'rt') as fh:
            return cls(json.loads(fh.read()))

    def __init__(self, data):

        """
        Read the compressed volume archive.

        Args:
            data (dict)
        """

        self.data = data

    def id(self):

        """
        Get the HTRC id.

        Returns: str
        """

        return self.data['id']

    def year(self):

        """
        Get the publication year.

        Returns: int
        """

        return int(self.data['metadata']['pubDate'])

    def language(self):

        """
        Get the language.

        Returns: str
        """

        return self.data['metadata']['language']

    def is_english(self):

        """
        Is the volume English?

        Returns: bool
        """

        return self.language() == 'eng'

    def token_count(self):

        """
        Get the total number of tokens in the page "body" sections.

        Returns: int
        """

        return sum([
            p.token_count()
            for p in self.pages()
        ])

    def pages(self):

        """
        Generate page instances.

        Yields: Page
        """

        for data in self.data['features']['pages']:
            yield Page(data)

    def token_offsets(self, resolution):

        """
        For each token, get the offsets of each instance of the token inside
        the text, with the offset is rounded to an integer.

        args:
            resolution (int)

        Returns: dict {token: Counter({ offset: count })}
        """

        offsets = defaultdict(Counter)

        token_count = self.token_count()

        seen = 0
        for page in self.pages():

            # 0-1 ratio of the page "center."
            center = (
                (seen + (page.token_count() / 2)) /
                token_count
            )

            offset = round(resolution * center)

            counts = page.merged_token_counts()

            # Register offset -> count.
            for token, count in counts.items():
                offsets[token][offset] += count

            # Track the cumulative count.
            seen += page.token_count()

        return offsets
