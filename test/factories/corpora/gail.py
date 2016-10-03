

import factory
import pkgutil

from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ListType

from jinja2 import Template

from .schematics import SchematicsFactory


class GailText(Model):

    id = StringType(required=True)

    title = StringType(required=True)

    year = IntType(required=True)

    tokens = ListType(StringType, min_size=1)

    def xml(self):

        """
        Render the XML template.

        Returns: str
        """

        raw = pkgutil.get_data(
            'test.factories.corpora',
            'templates/gail.j2',
        )

        template = Template(raw.decode('utf8'))

        # Render XML.
        return template.render(**dict(self))


class GailTextFactory(SchematicsFactory):

    class Meta:
        model = GailText

    id = factory.Sequence(lambda n: 'B000{0}'.format(n))

    title = 'Moby Dick'

    year = 1900

    tokens = ['Call', 'me', 'Ishmael.']
