

from lint.singletons import config
from lint.utils import round_to_decade, token_offset_counts

from lint.gail.corpus import Corpus
from lint.gail.text import Text

from .extract import Extract


class ExtractGail(Extract):

    def args(self):

        """
        Generate text paths.

        Yields: str
        """

        corpus = Corpus.from_env()

        yield from corpus.text_paths()

    def add_volume(self, path):

        """
        Increment offsets from a volume.

        Args:
            path (str)
        """

        text = Text(path)

        counts = token_offset_counts(
            text.plain_text(),
            config['offset_resolution'],
        )

        # Round to nearest decade.
        year = round_to_decade(text.year())

        # Merge counts into cache.
        self.cache.add_volume(year, counts)

    def flush(self):

        """
        Dump the offsets to disk.
        """

        self.cache.flush(config['results']['gail'])
