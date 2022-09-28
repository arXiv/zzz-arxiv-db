from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Table, Text, text, Enum
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata

class SubmissionClassifierData(Base):
    __tablename__ = 'arXiv_submission_classifier_data'

    submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True, server_default=text("'0'"))
    json = Column(Text)
    last_update = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    status = Column(Enum('processing', 'success', 'failed', 'no connection'))
    message = Column(Text)
    is_oversize = Column(TINYINT(1), server_default=text("'0'"))

    submission = relationship('Submissions', uselist=False)

from .. import Base

metadata = Base.metadata
