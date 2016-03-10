

import os

from zipfile import ZipFile
from invoke import task
from clint.textui import progress

from lint.harvest import Harvest


@task
def unzip():

    """
    Unzip the text files.
    """

    paths = list(Harvest().zip_paths)

    for path in progress.bar(paths):

        try:
            with ZipFile(path, 'r') as fh:
                fh.extractall(path='corpus')

        except: pass
