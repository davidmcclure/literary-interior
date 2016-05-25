

from invoke import task

from lint.models import BaseModel
from lint import config


@task
def init_db():

    """
    Create database tables.
    """

    engine = config.build_engine()

    BaseModel.metadata.create_all(engine)
