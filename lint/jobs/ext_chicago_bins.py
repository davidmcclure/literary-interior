

from lint.singletons import config
from lint.utils import round_to_decade

from lint.chicago.corpus import Corpus
from lint.chicago.novel import Novel
from lint.count_cache import CountCache
from lint.text import Text

from .scatter import Scatter


class ExtChicagoBins(Scatter):

    @classmethod
    def from_config(cls):

        """
        Apply config values.
        """

        return cls(
            result_dir=config['results']['bins']['chicago'],
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
        Generate text args.

        Yields: dict {corpus_path, metadata}
        """

        corpus = Corpus.from_env()

        for row in corpus.novels_metadata():
            yield dict(corpus_path=corpus.path, metadata=row)

    def process(self, corpus_path: str, metadata: dict):

        """
        Increment offsets from a volume.
        """

        novel = Novel.from_corpus_path(corpus_path, metadata)

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
