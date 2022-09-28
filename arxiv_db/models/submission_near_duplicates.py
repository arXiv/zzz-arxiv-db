from sqlalchemy import Column, ForeignKey, Index, TIMESTAMP, text
from sqlalchemy.dialects.mysql import DECIMAL, INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class SubmissionNearDuplicates(Base):
    __tablename__ = 'arXiv_submission_near_duplicates'
    __table_args__ = (
        Index('match', 'submission_id', 'matching_id', unique=True),
    )

    submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True, nullable=False, server_default=text("'0'"))
    matching_id = Column(INTEGER(11), primary_key=True, nullable=False, server_default=text("'0'"))
    similarity = Column(DECIMAL(2, 1), nullable=False)
    last_update = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    submission = relationship('Submissions')
