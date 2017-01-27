

from lint.singletons import config
from lint.utils import round_to_decade

from lint.count_cache import CountCache
from lint.models import Text

from .scatter import Scatter


class ExtBuckets(Scatter):

    @classmethod
    def from_config(cls):
        """Apply config values.
        """
        return cls(
            result_dir=config['results']['buckets'],
            bins=config['bins'],
        )

    def __init__(self, result_dir: str, bins: int):
        """Initialize the count cache.
        """
        self.result_dir = result_dir

        self.bins = bins

        self.cache = CountCache()

    def args(self):
        """Generate text ids.

        Returns: list
        """
        return Text.ids()

    def process(self, id: int):
        """Increment offsets from a volume.
        """
        text = Text.query.get(id)

        counts = text.bucket_counts(self.bins)

        # Round to nearest decade.
        year = round_to_decade(text.year)

        # Merge counts into cache.
        self.cache.add_token_counts(text.corpus, year, counts)

    def flush(self):
        """Dump the offsets to disk.
        """
        self.cache.flush(self.result_dir)
