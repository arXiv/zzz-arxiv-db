from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class SubmissionHoldReason(Base):
    __tablename__ = 'arXiv_submission_hold_reason'

    reason_id = Column(INTEGER(11), primary_key=True)
    submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('tapir_users.user_id', ondelete='CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    reason = Column(String(30))
    type = Column(String(30))
    comment_id = Column(ForeignKey('arXiv_admin_log.id'), index=True)

    comment = relationship('AdminLog')
    submission = relationship('Submissions')
    user = relationship('TapirUsers')
