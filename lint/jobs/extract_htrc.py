

from lint.singletons import config
from lint.htrc.manifest  import Manifest
from lint.htrc.volume import Volume
from lint.utils import round_to_decade

from .extract import Extract


class ExtractHTRC(Extract):

    def args(self):

        """
        Generate path segments.

        Returns: list
        """

        manifest = Manifest.from_env()

        return manifest.absolute_paths()

    def add_volume(self, path):

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
        offsets = vol.offset_counts(config['offset_resolution'])

        # Round to nearest decade.
        year = round_to_decade(vol.year())

        # Merge counts into cache.
        self.cache.add_volume(year, offsets)

    def flush(self):

        """
        Dump the offsets to disk.
        """

        self.cache.flush(config['results']['htrc'])
