from sqlalchemy import (
    Column,
    Integer,
    UnicodeText,
)

from .meta import Base


class Entry(Base):
    """A model for journal entries."""
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    title = Column(UnicodeText)
    body = Column(UnicodeText)
    creation_date = Column(UnicodeText)
