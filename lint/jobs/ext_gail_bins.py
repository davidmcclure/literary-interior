

from lint.singletons import config
from lint.utils import round_to_decade

from lint.gail.corpus import Corpus
from lint.gail.novel import Novel
from lint.count_cache import CountCache
from lint.text import Text

from .scatter import Scatter


class ExtGailBins(Scatter):

    @classmethod
    def from_config(cls):

        """
        Apply config values.
        """

        return cls(
            corpus_dir=config['gail'],
            result_dir=config['results']['bins']['gail'],
            bins=config['bins'],
        )

    def __init__(self, corpus_dir: str, result_dir: str, bins: int):

        """
        Initialize the count cache.
        """

        self.corpus_dir = corpus_dir

        self.result_dir = result_dir

        self.bins = bins

        self.cache = CountCache()

    def args(self):

        """
        Generate text paths.

        Yields: str
        """

        corpus = Corpus(self.corpus_dir)

        yield from corpus.text_paths()

    def process(self, path):

        """
        Increment offsets from a volume.

        Args:
            path (str)
        """

        novel = Novel.from_path(path)

        text = Text(novel.plain_text())

        counts = text.token_offset_counts(self.bins)

        # Round to nearest decade.
        year = round_to_decade(novel.year())

        # Merge counts into cache.
        self.cache.add_token_counts(year, counts)

    def flush(self):

        """
        Dump the offsets to disk.
        """

        self.cache.flush(self.result_dir)
