

from collections import defaultdict, Counter


class CountCache:


    def __init__(self):

        """
        Initialize the {year -> token -> offset -> count} map.
        """

        self.data = defaultdict(lambda: defaultdict(Counter))


    def __getitem__(self, key):

        """
        Alias the count data.

        Args:
            key (str)
        """

        return self.data[key]
