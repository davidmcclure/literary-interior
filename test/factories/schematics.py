

import factory


class SchematicsFactory(factory.Factory):

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        """
        Pass the kwargs straight into the Schematics class.

        Returns: model_class
        """

        return model_class(kwargs)
