from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class QuestionableCategories(Base):
    __tablename__ = 'arXiv_questionable_categories'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
    )

    archive = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    subject_class = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))

    arXiv_categories = relationship('Categories', uselist=False)
