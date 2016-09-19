

import factory

from lint.htrc.page import Page


class HTRCPageFactory(factory.Factory):

    class Meta:
        model = Page

    token_count = 100

    token_pos_count = {
        'word': {
            'POS': 1
        }
    }

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        """
        Construct a Page instance.

        Returns: Page
        """

        return model_class({
            'body': {
                'tokenCount': kwargs['token_count'],
                'tokenPosCount': kwargs['token_pos_count'],
            }
        })
