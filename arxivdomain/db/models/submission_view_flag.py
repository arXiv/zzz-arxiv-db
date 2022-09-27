from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class SubmissionViewFlag(Base):
    __tablename__ = 'arXiv_submission_view_flag'

    submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True, nullable=False)
    flag = Column(TINYINT(1), server_default=text("'0'"))
    user_id = Column(ForeignKey('tapir_users.user_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    updated = Column(DateTime)

    submission = relationship('Submissions')
    user = relationship('TapirUsers')
