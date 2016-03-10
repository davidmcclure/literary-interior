

import redis
import sys
import matplotlib.pyplot as plt
import numpy as np

from sklearn.neighbors import KernelDensity

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


    def kde(self, term, bandwidth=2000, samples=1000, kernel='gaussian'):

        """
        Estimate a density function for a term.

        Args:
            term (str): A stemmed term.
            bandwidth (int): The kernel bandwidth.
            samples (int): The number of sample points.
            kernel (str): The kernel function.

        Returns:
            np.array: The density estimate.
        """

        # Get the offsets of the term instances.
        terms = np.array(self.ratios[term])[:, np.newaxis]

        # Fit the density estimator on the terms.
        kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(terms)

        # Score an evely-spaced array of samples.
        x_axis = np.linspace(0, 1, samples)[:, np.newaxis]
        scores = kde.score_samples(x_axis)

        return np.exp(scores)


    def plot_kdes(self, terms, **kwargs):

        """
        Plot density estimates for set of terms.

        Args:
            terms (list): A list of terms.
        """

        for term in terms:
            kde = self.kde(term, **kwargs)
            plt.plot(kde)

        plt.show()
