

from lint.singletons import config
from lint.utils import round_to_decade, offset_counts

from lint.chicago.corpus import Corpus
from lint.chicago.novel import Novel

from .extract import Extract


class ExtractChicago(Extract):

    def args(self):

        """
        Generate text args.

        Yields: dict {corpus_path, metadata}
        """

        corpus = Corpus.from_env()

        for row in corpus.novels_metadata():
            yield dict(corpus_path=corpus.path, metadata=row)

    def add_volume(self, corpus_path, metadata):

        """
        Increment offsets from a volume.

        Args:
            path (str)
        """

        novel = Novel(corpus_path, metadata)

        counts = offset_counts(
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