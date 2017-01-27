

import factory
import uuid

from lint.htrc.page import Page
from lint.htrc.volume import Volume


class HTRCPageFactory(factory.Factory):

    class Meta:
        model = Page

    token_count = 100

    counts = {
        'word': {
            'POS': 1
        }
    }

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        """
        Returns: Page
        """

        return model_class({
            'body': {
                'tokenCount': kwargs['token_count'],
                'tokenPosCount': kwargs['counts'],
            }
        })


class HTRCVolumeFactory(factory.Factory):

    class Meta:
        model = Volume

    id = factory.LazyAttribute(lambda v: str(uuid.uuid4()))

    year = 1900

    language = 'eng'

    pages = []

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Returns: Volume
        """
        return model_class({

            'id': kwargs['id'],

            'metadata': {
                'pubDate': str(kwargs['year']),
                'language': kwargs['language'],
            },

            'features': {
                'pages': [p.data for p in kwargs['pages']]
            },

        })
