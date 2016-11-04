

from lint.singletons import config

from lint.text import Text
from lint.gail.corpus import Corpus
from lint.gail.novel import Novel

from .scatter import Scatter


class ExtGailTokens(Scatter):

    def __init__(self, corpus_dir: str):

        """
        Set the corpus directory.
        """

        self.corpus_dir = corpus_dir

    def args(self):

        """
        Generate text paths.

        Yields: str
        """

        corpus = Corpus(self.corpus_dir)

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
