

import pytest
import os

from lint.singletons import config as _config, session
from lint.models import Base

from test.mock_results import MockResults
from test.mock_corpus import MockCorpus


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
def mock_corpus(config):

    """
    Yields: MockCorpus
    """

    corpus = MockCorpus()

    config.config['htrc']['features'] = corpus.features_path
    config.config['htrc']['manifest'] = corpus.manifest_path

    yield corpus

    corpus.teardown()


@pytest.yield_fixture
def mock_results(config):

    """
    Yields: MockResults
    """

    results = MockResults()

    config.config['offsets']['htrc'] = results.path

    yield results

    results.teardown()


@pytest.yield_fixture
def mpi(mock_corpus, mock_results, config):

    """
    Write the current configuration into the /tmp/.lint.yml file.
    """

    config.write_tmp()

    yield

    config.clear_tmp()

    session.remove()

    init_testing_db()
