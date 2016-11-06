

import os
import uuid
import json

from lint.singletons import config
from lint.chicago.novel import Novel
from lint.chicago.corpus import Corpus
from lint.models import Text

from .scatter import Scatter


class ExtChicagoTexts(Scatter):

    @classmethod
    def from_config(cls):

        """
        Apply config values.
        """

        return cls(
            corpus_dir=config['chicago'],
            result_dir=config['results']['texts'],
        )

    def __init__(self, corpus_dir: str, result_dir: str):

        """
        Set input / output directories.
        """

        self.corpus_dir = corpus_dir

        self.result_dir = result_dir

    def args(self):

        """
        Generate text args.

        Yields: dict {corpus_path, metadata}
        """

        corpus = Corpus(self.corpus_dir)

        for row in corpus.novels_metadata():
            yield dict(corpus_path=corpus.path, metadata=row)

    def process(self, corpus_path: str, metadata: dict):

        """
        Extract text metadata.
        """

        novel = Novel.from_corpus_path(corpus_path, metadata)

        text = dict(
            corpus='chicago',
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
