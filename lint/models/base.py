

from sqlalchemy.ext.declarative import declarative_base

from lint.singletons import session


class _Base:

    def columns(self):

        """
        Get a list of column names.

        Returns: list
        """

        return [c.name for c in self.__table__.columns]

    def __iter__(self):

        """
        Generate column / value tuples.

        Yields: (key, val)
        """

        for key in self.columns():
            yield (key, getattr(self, key))


Base = declarative_base(cls=_Base)

Base.query = session.query_property()
