

import os

from invoke import task

from lint.corpus import Corpus


@task
def count():

    """
    How many zip files are in the corpus?
    """

    paths = Corpus().paths('.zip')

    print(len(list(paths)))


@task
def unzip():

    """
    Unzip the text files.
    """

    pass
