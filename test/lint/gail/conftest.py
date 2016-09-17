

import pytest

from lint.gail.text import Text


@pytest.fixture
def gail_text(fixture_path):

    """
    Given a Gail id, provide a fixture path.
    """

    def func(slug):

        parts = slug.split('-')

        # Form the Gail file path.
        rel_path = 'gail-amfic/{0}-{1}/Monographs/{2}.xml'.format(
            parts[0], parts[1], slug
        )

        return Text(fixture_path(rel_path))

    return func
