

from lint.count_cache import CountCache


class IndexCount:


    def __init__(self, out_path, group_size=1000):

        """
        Set options, initialize the cache.

        Args:
            out_path (str)
            group_size (int)
        """

        self.out_path = out_path

        self.group_size = group_size

        self.cache = CountCache()


    def run(self):

        """
        Extract {year -> token -> offset -> count} for all volumes.
        """

        pass
