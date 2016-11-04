

import os
import pickle
import uuid

from lint.singletons import config

from lint.text import Text
from lint.gail.novel import Novel
from lint.gail.corpus import Corpus
from lint.models import Token

from .scatter import Scatter


class ExtGailTokens(Scatter):

    @classmethod
    def from_config(cls):

        """
        Apply config values.
        """

        return cls(
            corpus_dir=config['gail'],
            result_dir=config['results']['tokens']['gail'],
        )

    def __init__(self, corpus_dir: str, result_dir: str):

        """
        Set the corpus directory.
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
        Extract tokens from a text.

        Args:
            path (str)
        """

        novel = Novel.from_path(path)

        identifier = novel.identifier()

        year = novel.year()

        text = Text(novel.plain_text())

        tags = text.pos_tags()

        # Assemble token list.

        # TODO: Where to thread in the ratio?

        tokens = [

            dict(
                corpus='gail',
                identifier=identifier,
                year=year,
                ratio=i/len(tags),
                **tag._asdict(),
            )

            for i, tag in enumerate(tags)

        ]

        # Flush to disk.

        path = os.path.join(self.result_dir, str(uuid.uuid4()))

        with open(path, 'wb') as fh:
            pickle.dump(tokens, fh)
