

from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint

from lint.models import Base


class Char(Base):


    __tablename__ = 'char'

    __table_args__ = (
        PrimaryKeyConstraint(
            'corpus',
            'year',
            'char',
            'offset',
        ),
    )

    corpus = Column(String, nullable=False)

    year = Column(Integer, nullable=False)

    char = Column(String, nullable=False)

    offset = Column(Integer, nullable=False)

    count = Column(Integer, nullable=False)
