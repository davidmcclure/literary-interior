

import pytest
import os

from lint.singletons import config as _config, session
from lint.models import Base

from test.result_dir import ResultDir
from test.htrc_data import HTRCData
from test.chicago_data import ChicagoData
from test.gail_data import GailData


@pytest.fixture(scope='session', autouse=True)
def init_testing_db():
    """Drop and recreate the tables.
    """
    engine = _config.build_sqla_engine()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.yield_fixture
def db():
    """Reset the testing database.
    """
    session.begin_nested()

    yield

    session.remove()


@pytest.yield_fixture
def config():
    """Clear changes to the config dict.
    """
    # Copy settings.
    old = _config.copy()

    yield _config

    # Restore settings.
    _config.clear()
    _config.update(old)


@pytest.yield_fixture
def htrc_data(config):
    """Yields: HTRCData
    """
    corpus = HTRCData()

    config['htrc']['features'] = corpus.features_path
    config['htrc']['manifest'] = corpus.manifest_path

    yield corpus

    corpus.teardown()


@pytest.yield_fixture
def chicago_data(config):
    """Yields: ChicagoData
    """
    corpus = ChicagoData()

    config['chicago'] = corpus.path

    yield corpus

    corpus.teardown()


@pytest.yield_fixture
def gail_data(config):
    """Yields: GailData
    """
    corpus = GailData()

    config['gail'] = corpus.path

    yield corpus

    corpus.teardown()


@pytest.fixture
def mock_result_dir(config):
    """Yields: ResultDir
    """

    def func(rtype):

        results = ResultDir()

        config['results'][rtype] = results.path

        yield results

        results.teardown()

    return func


@pytest.yield_fixture
def text_results(mock_result_dir):
    yield from mock_result_dir('texts')


@pytest.yield_fixture
def bucket_results(mock_result_dir):
    yield from mock_result_dir('buckets')


@pytest.yield_fixture
def token_results(mock_result_dir):
    yield from mock_result_dir('tokens')


@pytest.yield_fixture
def mpi(

    config,

    # Mock all data sources + result dirs.

    htrc_data,
    chicago_data,
    gail_data,

    text_results,
    bucket_results,
    token_results,

):
    """Write the patched config to /tmp/.lint.yml.
    """
    config.write_tmp()

    yield

    config.clear_tmp()

    session.remove()

    init_testing_db()
