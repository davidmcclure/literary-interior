

import os

from zipfile import ZipFile
from invoke import task
from clint.textui import progress

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

    paths = list(Corpus().paths('.zip'))

    for path in progress.bar(paths):
        with ZipFile(path, 'r') as fh:
            fh.extractall(path=os.path.dirname(path))
