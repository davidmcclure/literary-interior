

import pytest
import os

from lint.singletons import config as _config, session
from lint.models import Base

from test.result_dir import ResultDir
from test.htrc_data import HTRCData
from test.chicago_data import ChicagoData


@pytest.fixture(scope='session', autouse=True)
def init_testing_db():

    """
    Drop and recreate the tables.
    """

    engine = _config.build_sqla_engine()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.yield_fixture
def db():

    """
    Reset the testing database.
    """

    session.begin_nested()

    yield

    session.remove()


@pytest.yield_fixture
def config():

    """
    Clear changes to the config dict.
    """

    old = _config.config.copy()

    yield _config

    _config.config = old


@pytest.yield_fixture
def htrc_data(config):

    """
    Yields: HTRCData
    """

    corpus = HTRCData()

    config.config['htrc']['features'] = corpus.features_path
    config.config['htrc']['manifest'] = corpus.manifest_path

    yield corpus

    corpus.teardown()


@pytest.yield_fixture
def chicago_data(config):

    """
    Yields: ChicagoData
    """

    corpus = ChicagoData()

    config.config['chicago'] = corpus.path

    yield corpus

    corpus.teardown()


@pytest.yield_fixture
def htrc_results(config):

    """
    Yields: ResultDir
    """

    results = ResultDir()

    config.config['results']['htrc'] = results.path

    yield results

    results.teardown()


@pytest.yield_fixture
def chicago_results(config):

    """
    Yields: ResultDir
    """

    results = ResultDir()

    config.config['results']['chicago'] = results.path

    yield results

    results.teardown()


@pytest.yield_fixture
def mpi(htrc_data, chicago_data, htrc_results, chicago_results, config):

    # TODO: Use htrc_mpi, chicago_mpi, etc?

    """
    Write the current configuration into the /tmp/.lint.yml file.
    """

    config.write_tmp()

    yield

    config.clear_tmp()

    session.remove()

    init_testing_db()


@pytest.fixture
def fixture_path():

    """
    Provide a helper function that provides an absolute fixture path.
    """

    def func(rel_path):

        # ./fixtures
        dir_path = os.path.join(os.path.dirname(__file__), 'fixtures')

        return os.path.join(dir_path, rel_path)

    return func
