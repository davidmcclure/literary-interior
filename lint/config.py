

import os
import anyconfig
import yaml

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL

from wordfreq import top_n_list
from contextlib import contextmanager


# TODO: Use singletons module, scoped session.


class Config:

    TMP_YAML = '/tmp/.lint.yml'

    @classmethod
    def from_env(cls):

        """
        Get a config instance with the default files.
        """

        # Default paths.
        paths = [
            os.path.join(os.path.dirname(__file__), 'lint.yml'),
            '~/.lint.yml',
        ]

        # Base testing config.
        if os.environ.get('LINT_ENV') == 'test':
            paths.append('~/.lint.test.yml')

        # Per-test overrides.
        paths.append(cls.TMP_YAML)

        return cls(paths)

    def __init__(self, paths):

        """
        Initialize the configuration object.

        Args:
            paths (list): YAML paths, from most to least specific.
        """

        self.config = anyconfig.load(paths, ignore_missing=True)

    def __getitem__(self, key):

        """
        Get a configuration value.

        Args:
            key (str): The configuration key.

        Returns:
            The option value.
        """

        return self.config.get(key)

    def build_sqla_url(self):

        """
        Build a SQLAlchemy connection string.

        Returns: Engine
        """

        return URL(**self['database'])

    def build_sqla_engine(self):

        """
        Build a SQLAlchemy engine.

        Returns: Engine
        """

        url = self.build_sqla_url()

        engine = create_engine(url)

        # Fix transaction bugs in pysqlite.
        # http://docs.sqlalchemy.org/en/rel_1_0/dialects/sqlite.html#pysqlite-serializable

        @event.listens_for(engine, 'connect')
        def connect(conn, record):
            conn.isolation_level = None

        @event.listens_for(engine, 'begin')
        def begin(conn):
            conn.execute('BEGIN')

        return engine

    def build_sqla_sessionmaker(self):

        """
        Build a SQLAlchemy session class.

        Returns: Session
        """

        return sessionmaker(bind=self.build_sqla_engine())

    def build_sqla_session(self):

        """
        Build a scoped session manager.

        Returns: Session
        """

        return scoped_session(self.build_sqla_sessionmaker())

    def build_tokens(self):

        """
        Get a set of whitelisted tokens.

        Returns: set
        """

        tokens = top_n_list('en', self['token_depth'], ascii_only=True)

        return set(tokens)

    def write_tmp(self):

        """
        Write the config into the /tmp file.
        """

        with open(self.TMP_YAML, 'w') as fh:
            fh.write(yaml.dump(self.config))

    def clear_tmp(self):

        """
        Clear the /tmp file.
        """

        os.remove(self.TMP_YAML)
