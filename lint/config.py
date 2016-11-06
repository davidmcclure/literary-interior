

import os
import anyconfig
import yaml

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.url import URL


class Config(dict):

    TMP_YAML = '/tmp/.lint.yml'

    @classmethod
    def from_env(cls):

        """
        Get a config instance with the default files.
        """

        root = os.environ.get('LINT_CONFIG', '~/.lint')

        # Default paths.
        paths = [
            os.path.join(os.path.dirname(__file__), 'lint.yml'),
            os.path.join(root, 'lint.yml'),
        ]

        # Patch in the testing config.
        if os.environ.get('LINT_ENV') == 'test':
            paths.append(os.path.join(root, 'lint.test.yml'))

        # MPI overrides.
        paths.append(cls.TMP_YAML)

        return cls(paths)

    def __init__(self, paths):

        """
        Initialize the configuration object.

        Args:
            paths (list): YAML paths, from most to least specific.
        """

        config = anyconfig.load(paths, ignore_missing=True)

        return super().__init__(config)

    def build_sqla_url(self):

        """
        Build a SQLAlchemy connection string.

        Returns: Engine
        """

        return URL(**dict(
            drivername='sqlite',
            database=self['database'],
        ))

    def build_sqla_engine(self):

        """
        Build a SQLAlchemy engine.

        Returns: Engine
        """

        url = self.build_sqla_url()

        engine = create_engine(url)

        # Fix transaction bugs in pysqlite.

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

    def write_tmp(self):

        """
        Write the config into the /tmp file.
        """

        with open(self.TMP_YAML, 'w') as fh:
            fh.write(yaml.dump(self))

    def clear_tmp(self):

        """
        Clear the /tmp file.
        """

        os.remove(self.TMP_YAML)
