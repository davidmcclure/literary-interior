

import tempfile
import shutil


class TempDir:

    def __init__(self):

        """
        Create the temporary directory.
        """

        self.path = tempfile.mkdtemp()

    def teardown(self):

        """
        Delete the temporary directory.
        """

        shutil.rmtree(self.path)
