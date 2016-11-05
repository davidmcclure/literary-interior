

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    PrimaryKeyConstraint,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from lint.models import Base


class Token(Base):

    __tablename__ = 'token'

    __table_args__ = (
        PrimaryKeyConstraint(
            'text_id',
            'token',
            'offset',
        ),
    )

    text_id = Column(Integer, ForeignKey('text.id'))

    text = relationship('Text')

    token = Column(String, nullable=False)

    offset = Column(Integer, nullable=False)

    ratio = Column(Integer, nullable=False)
