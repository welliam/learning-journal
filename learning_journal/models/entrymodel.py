from sqlalchemy import (
    Column,
    Integer,
    UnicodeText,
)

from .meta import Base


class EntryModel(Base):
    """A model for journal entries."""
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(UnicodeText)
    body = Column(UnicodeText)
    date = Column(UnicodeText)
