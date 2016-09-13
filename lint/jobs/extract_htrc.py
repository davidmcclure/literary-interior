

from lint.singletons import config
from lint.htrc.manifest  import Manifest
from lint.htrc.volume import Volume
from lint.utils import round_to_decade

from .extract import Extract


class ExtractHTRC(Extract):

    def segments(self, size):

        """
        Generate path segments.

        Args:
            size (int)

        Returns: list
        """

        manifest = Manifest.from_env()

        return manifest.json_segments(size)

    def increment(self, path):

        """
        Increment offsets from a volume.

        Args:
            path (str)
        """

        vol = Volume.from_path(path)

        # Ignore non-English vols.
        if not vol.is_english():
            return

        # Get token offset counts.
        offsets = vol.token_offsets(config['offset_resolution'])

        # Round to nearest decade.
        year = round_to_decade(vol.year())

        # Merge counts into cache.
        self.cache.increment(year, offsets)

    def flush(self):

        """
        Dump the offsets to disk.
        """

        self.cache.flush(config['results']['htrc'])
