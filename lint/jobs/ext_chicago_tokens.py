

from lint.singletons import config
from lint.utils import round_to_decade, token_offset_counts

from lint.chicago.corpus import Corpus
from lint.chicago.novel import Novel
from lint.count_cache import CountCache

from .scatter import Scatter


class ExtChicagoTokens(Scatter):

    def __init__(self):

        """
        Initialize the count cache.
        """

        self.cache = CountCache()

    def args(self):

        """
        Generate text args.

        Yields: dict {corpus_path, metadata}
        """

        corpus = Corpus.from_env()

        for row in corpus.novels_metadata():
            yield dict(corpus_path=corpus.path, metadata=row)

    def process(self, corpus_path, metadata):

        """
        Increment offsets from a volume.

        Args:
            path (str)
        """

        novel = Novel(corpus_path, metadata)

        counts = token_offset_counts(
            novel.source_text(),
            config['offset_resolution'],
        )

        # Round to nearest decade.
        year = round_to_decade(novel.year())

        # Merge counts into cache.
        self.cache.add_volume(year, counts)

    def flush(self):

        """
        Dump the offsets to disk.
        """

        self.cache.flush(config['results']['chicago'])
