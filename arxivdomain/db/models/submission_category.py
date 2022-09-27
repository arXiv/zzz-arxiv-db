from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class SubmissionCategory(Base):
    __tablename__ = 'arXiv_submission_category'

    submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    category = Column(ForeignKey('arXiv_category_def.category'), primary_key=True, nullable=False, index=True, server_default=text("''"))
    is_primary = Column(TINYINT(1), nullable=False, index=True, server_default=text("'0'"))
    is_published = Column(TINYINT(1), index=True, server_default=text("'0'"))

    arXiv_category_def = relationship('CategoryDef')
    submission = relationship('Submissions')
