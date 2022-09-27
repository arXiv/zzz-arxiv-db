from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class SubmissionModHold(Base):
    __tablename__ = 'arXiv_submission_mod_hold'

    submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True)
    reason = Column(String(30))
    comment_id = Column(ForeignKey('arXiv_admin_log.id'), nullable=False, index=True)

    comment = relationship('AdminLog')
    submission = relationship('Submissions', uselist=False)
