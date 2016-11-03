

import factory
import pkgutil

from jinja2 import Template

from lint.gail.novel import Novel


class GailNovelFactory(factory.Factory):

    class Meta:
        model = Novel

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
