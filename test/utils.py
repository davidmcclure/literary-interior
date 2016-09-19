

import uuid

from lint.htrc.page import Page
from lint.htrc.volume import Volume


def make_htrc_vol(pages=[], year=1900, language='eng', id=None):

    """
    Make a volume instance with the provided tokenPosCount maps.

    Args:
        pages (list)
        year (int)
        language (str)
        id (str)

    Returns: Volume
    """

    if not id:
        id = str(uuid.uuid4())

    data = {

        'id': id,

        'metadata': {
            'pubDate': str(year),
            'language': language,
        },

        'features': {
            'pages': [p.data for p in pages]
        },

    }

    return Volume(data)
