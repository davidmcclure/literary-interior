

import os
import anyconfig
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wordfreq import top_n_list
from contextlib import contextmanager


class Config:


    TMP_YAML = '/tmp/.lint.yml'


    @classmethod
    def from_env(cls):

        """
        Get a config instance with the default files.
        """

        return cls([
            os.path.join(os.path.dirname(__file__), 'lint.yml'),
            '~/.lint.yml',
            cls.TMP_YAML,
        ])


    def __init__(self, paths):

        """
        Initialize the configuration object.

        Args:
            paths (list): YAML paths, from most to least specific.
        """

        self.paths = paths

        self.read()


    def __getitem__(self, key):

        """
        Get a configuration value.

        Args:
            key (str): The configuration key.

        Returns:
            The option value.
        """

        return self.config.get(key)


    def read(self):

        """
        Load the configuration files, set globals.
        """

        # Parse the configuration.
        self.config = anyconfig.load(self.paths, ignore_missing=True)

        # Canonical set of tokens.
        self.tokens = self.build_tokens()

        # SQLAlchemy session maker.
        self.Session = self.build_sessionmaker()


    def build_tokens(self):

        """
        Get a set of whitelisted tokens.

        Returns: set
        """

        tokens = top_n_list('en', self['token_depth'], ascii_only=True)

        return set(tokens)


    def build_engine(self):

        """
        Build a SQLAlchemy engine.

        Returns: Engine
        """

        return create_engine(self['database'])


    def build_sessionmaker(self):

        """
        Build a SQLAlchemy session class.

        Returns: Session
        """

        return sessionmaker(bind=self.build_engine())


    @contextmanager
    def get_session(self):

        """
        Provide a transactional scope around a query.

        Yields: Session
        """

        session = self.Session()

        try:
            yield session
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()


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
