

import redis
import sys

from .corpus import Corpus


class Ratios:


    def __init__(self):

        """
        Connect to Redis.
        """

        self.redis = redis.StrictRedis()


    def index(self):

        """
        Index combined offsets.
        """

        corpus = Corpus()

        for text in corpus.texts:

            pipe = self.redis.pipeline()

            # Register the terms.
            pipe.sadd(
                'lint:terms',
                *list(text.ratios.keys()),
            )

            for term, ratios in text.ratios.items():

                # Append the ratios.
                pipe.rpush(
                    'lint:ratios:{0}'.format(term),
                    *ratios,
                )

            # Batch update all words.
            pipe.execute()


    def ratios(self, term):

        """
        Get all ratios for a term.

        Args:
            term (str)

        Returns: list<float>
        """

        ratios = self.redis.lrange(
            'lint:ratios:{0}'.format(term),
            0, -1,
        )

        # Cast back to floats, sort.
        return sorted([float(r) for r in ratios])


    @property
    def terms(self):

        """
        Get all terms.

        Returns: list
        """

        return self.redis.smembers('lint:terms')
