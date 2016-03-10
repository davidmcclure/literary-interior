

import redis
import sys

from .corpus import Corpus


class Ratios:


    def __init__(self):

        """
        Initialize ratios dict.
        """

        self.ratios = {}


    def index(self):

        """
        Index combined offsets.
        """

        corpus = Corpus()

        for text in corpus.texts:
            for term, ratios in text.ratios.items():

                # Update existing term.
                if term in self.ratios:
                    self.ratios[term] += ratios

                # Initialize new term.
                else:
                    self.ratios[term] = ratios
