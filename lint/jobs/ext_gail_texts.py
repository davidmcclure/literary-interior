

import os
import uuid
import json

from lint.singletons import config
from lint.gail.novel import Novel
from lint.gail.corpus import Corpus
from lint.models import Text

from .scatter import Scatter


class ExtGailTexts(Scatter):

    @classmethod
    def from_config(cls):

        """
        Apply config values.
        """

        return cls(
            corpus_dir=config['gail'],
            result_dir=config['results']['texts']['gail'],
        )

    def __init__(self, corpus_dir: str, result_dir: str):

        """
        Set input / output directories.
        """

        self.corpus_dir = corpus_dir

        self.result_dir = result_dir

    def args(self):

        """
        Generate text paths.

        Yields: str
        """

        corpus = Corpus(self.corpus_dir)

        yield from corpus.text_paths()

    def process(self, path):

        """
        Extract text metadata.

        Args:
            path (str)
        """

        novel = Novel.from_path(path)

        text = dict(
            corpus='gail',
            identifier=novel.identifier(),
            year=novel.year(),
            title=novel.title(),
            author_first=novel.author_first(),
            author_last=novel.author_last(),
            text=novel.plain_text(),
        )

        path = os.path.join(self.result_dir, str(uuid.uuid4()))

        with open(path, 'w') as fh:
            json.dump(text, fh)
