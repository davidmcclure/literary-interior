

import pytest

from lint import config as _config
from lint.models import BaseModel


@pytest.fixture(scope='session', autouse=True)
def test_env():

    """
    Register the testing config file.
    """

    _config.paths.append('~/.lint.test.yml')
    _config.read()


@pytest.yield_fixture
def config():

    """
    Reset the configuration object after each test.

    Yields:
        The modify-able config object.
    """

    yield _config
    _config.read()


@pytest.fixture()
def db(config):

    """
    Create / reset the testing database.
    """

    engine = config.build_engine()

    # Clear and recreate all tables.
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
