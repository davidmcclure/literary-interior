

import os

from invoke import task


@task
def count():

    """
    How many zip files are in the corpus?
    """

    count = 0

    for root, dirs, files in os.walk('corpus'):

        for f in files:
            base, ext = os.path.splitext(f)
            if ext == '.zip': count += 1

    print(count)
