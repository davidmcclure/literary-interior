

from test.temp_dir import TempDir


class MockResults(TempDir):

    def add_cache(self, cache):

        """
        Pickle a cache into the directory.

        Args:
            cache (OffsetCache)
        """

        cache.flush(self.path)
