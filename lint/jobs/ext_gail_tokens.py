

from lint.singletons import config

from lint.text import Text
from lint.gail.corpus import Corpus

from .scatter import Scatter


class ExtGailBins(Scatter):

    def args(self):

        """
        Generate text paths.

        Yields: str
        """

        corpus = Corpus.from_env()

        yield from corpus.text_paths()

    def process(self, path):

        """
        Extract tokens from a text.

        Args:
            path (str)
        """

        novel = Novel.from_path(path)

        text = Text(novel.plain_text())

        print(text.pos_tags())
