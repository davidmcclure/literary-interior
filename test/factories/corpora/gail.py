

import factory
import pkgutil

from jinja2 import Template

from lint.gail.text import Text


class GailTextFactory(factory.Factory):

    class Meta:
        model = Text

    id = factory.Sequence(lambda n: 'B000{0}'.format(n))

    title = 'Moby Dick'

    year = 1900

    tokens = ['Call', 'me', 'Ishmael.']

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        """
        Returns: Text
        """

        # Read XML template.
        raw = pkgutil.get_data(
            'test.factories.corpora',
            'templates/gail.j2',
        )

        # Compile template.
        template = Template(raw.decode('utf8'))

        # Render XML.
        xml = template.render(**kwargs)

        return model_class(xml)
