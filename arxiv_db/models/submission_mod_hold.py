from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class SubmissionModHold(Base):
    __tablename__ = 'arXiv_submission_mod_hold'

    submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE'), primary_key=True)
    reason = Column(String(30))
    comment_id = Column(ForeignKey('arXiv_admin_log.id'), nullable=False, index=True)

    comment = relationship('AdminLog')
    submission = relationship('Submissions', uselist=False)
