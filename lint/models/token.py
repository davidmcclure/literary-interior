

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

from lint.models import Base


class Token(Base):


    __tablename__ = 'token'

    __table_args__ = (
        PrimaryKeyConstraint(
            'corpus',
            'year',
            'token',
            'pos',
        ),
    )

    corpus = Column(String, nullable=False)

    identifier = Column(String, nullable=False)

    year = Column(Integer, nullable=False)

    token = Column(String, nullable=False)

    pos = Column(String, nullable=False)

    # TODO: positions?
