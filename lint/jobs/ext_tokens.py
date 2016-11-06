

import os
import json
import uuid

from lint.singletons import config
from lint.models import Text

from .scatter import Scatter


class ExtTokens(Scatter):

    @classmethod
    def from_config(cls):

        """
        Apply config values.
        """

        return cls(result_dir=config['results']['tokens'])

    def __init__(self, result_dir: str):

        """
        Set the result dir.
        """

        self.result_dir = result_dir

    def args(self):

        """
        Generate text ids.

        Returns: list
        """

        return Text.ids()

    def process(self, id: int):

        """
        Increment offsets from a volume.
        """

        text = Text.query.get(id)

        tags = text.pos_tags()

        # Assemble token list.

        tokens = [

            dict(

                text_id=id,
                **tag._asdict(),

                offset=i,
                ratio=i/len(tags),

            )

            for i, tag in enumerate(tags)

        ]

        # Flush to disk.

        path = os.path.join(self.result_dir, str(uuid.uuid4()))

        with open(path, 'w') as fh:
            json.dump(tokens, fh)
