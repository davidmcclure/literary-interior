

from test.temp_dir import TempDir


class ResultDir(TempDir):

    def add_cache(self, cache):

        """
        Pickle a cache into the directory.

        Args:
            cache (CountCache)
        """

        cache.flush(self.path)
