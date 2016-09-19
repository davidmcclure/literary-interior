

import factory

from schematics.models import Model
from schematics.types import IntType, StringType
from schematics.types.compound import ListType

from .schematics import SchematicsFactory


class GailText(Model):

    id = StringType(required=True)

    title = StringType(required=True)

    year = IntType(required=True)

    tokens = ListType(StringType, min_size=1)


class GailTextFactory(SchematicsFactory):

    class Meta:
        model = GailText

    id = factory.Sequence(lambda n: 'B000{0}'.format(n))

    title = 'Moby Dick'

    year = 1900

    tokens = ['Call', 'me', 'Ishmael.']
