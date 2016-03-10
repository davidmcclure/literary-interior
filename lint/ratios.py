

import redis

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

            for token, ratios in text.ratios.items():
                self.add_ratios(token, ratios)


    def add_ratios(self, token, ratios):

        """
        Push on a new set of ratios for a word type.

        Args:
            token (str)
            ratios (list<float>)
        """

        self.redis.rpush(
            'ratios:{0}'.format(token),
            *ratios,
        )


    def get_ratios(self, token):

        """
        Get all ratios for a token.

        Returns: list<float>
        """

        ratios = self.redis.lrange('ratios:{0}'.format(token), 0, -1)

        # Cast back to floats.
        return [float(r) for r in ratios]
