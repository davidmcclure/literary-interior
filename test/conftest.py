

import pytest
import os

from lint import config as _config
from lint.models import BaseModel

from test.mock_results import MockResults
from test.mock_corpus import MockCorpus


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


@pytest.yield_fixture
def mock_results(config):

    """
    Provide a MockResults instance.

    Yields: MockResults
    """

    results = MockResults()

    config.config.update({
        'result_dir': results.path
    })

    yield results

    results.teardown()


@pytest.yield_fixture
def mock_corpus(config):

    """
    Provide a MockCorpus instance.

    Yields: MockCorpus
    """

    corpus = MockCorpus()

    config.config.update({
        'corpus_dir': corpus.path
    })

    yield corpus

    corpus.teardown()


@pytest.yield_fixture()
def mpi(mock_corpus, mock_results, config):

    """
    Write the current configuration into the /tmp/.lint.yml file.
    """

    config.write_tmp()

    yield

    config.clear_tmp()
