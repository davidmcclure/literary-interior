

from collections import defaultdict, Counter

from lint.utils import flatten_dict


class CountCache(defaultdict):


    def __init__(self):

        """
        Initialize the {year -> token -> offset -> count} map.
        """

        super().__init__(lambda: defaultdict(Counter))


    def flatten(self):

        """
        Flatten the cache into tuples.

        Yields: tuple (year, token, offset, count)
        """

        return flatten_dict(self)
