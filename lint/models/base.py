

from sqlalchemy.ext.declarative import declarative_base

from lint.singletons import session


Base = declarative_base()

Base.query = session.query_property()
