

from lint.singletons import config
from lint.htrc.manifest  import Manifest
from lint.htrc.volume import Volume
from lint.count_cache import CountCache
from lint.utils import round_to_decade

from .scatter import Scatter


class ExtHTRCBins(Scatter):

    @classmethod
    def from_config(cls):

        """
        Apply config values.
        """

        return cls(
            result_dir=config['results']['bins']['htrc'],
            bins=config['bins'],
        )

    def __init__(self, result_dir: str, bins: int):

        """
        Initialize the count cache.
        """

        self.result_dir = result_dir

        self.bins = bins

        self.cache = CountCache()

    def args(self):

        """
        Generate volume paths.

        Yields: str
        """

        manifest = Manifest.from_env()

        yield from manifest.absolute_paths()

    def process(self, path):

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
        offsets = vol.offset_counts(self.bins)

        # Round to nearest decade.
        year = round_to_decade(vol.year())

        # Merge counts into cache.
        self.cache.add_token_counts(year, offsets)

    def flush(self):

        """
        Dump the offsets to disk.
        """

        self.cache.flush(self.result_dir)
