

from invoke import task

from lint.singletons import config
from lint.models import Base


@task
def init_db(ctx):

    """
    Create database tables.
    """

    engine = config.build_sqla_engine()

    Base.metadata.create_all(engine)
