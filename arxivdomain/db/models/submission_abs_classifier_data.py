from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class SubmissionAbsClassifierData(Base):
    __tablename__ = 'arXiv_submission_abs_classifier_data'

    submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True, server_default=text("'0'"))
    json = Column(Text)
    last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Enum('processing', 'success', 'failed', 'no connection'))
    message = Column(Text)
    is_oversize = Column(TINYINT(1), server_default=text("'0'"))
    suggested_primary = Column(Text)
    suggested_reason = Column(Text)
    autoproposal_primary = Column(Text)
    autoproposal_reason = Column(Text)
    classifier_service_version = Column(Text)
    classifier_model_version = Column(Text)

    submission = relationship('Submissions', uselist=False)
