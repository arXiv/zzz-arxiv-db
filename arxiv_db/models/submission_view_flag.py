from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

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
