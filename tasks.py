

import os

from invoke import task


@task
def unzip():

    """
    Unzip Gutenberg files.
    """

    for root, dirs, files in os.walk('corpus'):
        print(files)
