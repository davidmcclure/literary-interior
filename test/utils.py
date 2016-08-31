

import uuid

from lint.htrc.page import Page
from lint.htrc.volume import Volume


def make_page(counts={}, token_count=100):

    """
    Make a page instance with the provided tokenPosCount map.

    Args:
        counts (dict)

    Returns: Page
    """

    return Page({
        'body': {
            'tokenCount': token_count,
            'tokenPosCount': counts,
        }
    })


def make_vol(pages=[], year=1900, language='eng', id=None):

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
