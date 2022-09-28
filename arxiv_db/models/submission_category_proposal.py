from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class SubmissionCategoryProposal(Base):
    __tablename__ = 'arXiv_submission_category_proposal'

    proposal_id = Column(INTEGER(11), primary_key=True, nullable=False, index=True, autoincrement=True)
    submission_id = Column(ForeignKey('arXiv_submissions.submission_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    category = Column(ForeignKey('arXiv_category_def.category'), primary_key=True, nullable=False, index=True)
    is_primary = Column(TINYINT(1), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    proposal_status = Column(INTEGER(11), server_default=text("'0'"))
    user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True)
    updated = Column(DateTime)
    proposal_comment_id = Column(ForeignKey('arXiv_admin_log.id'), index=True)
    response_comment_id = Column(ForeignKey('arXiv_admin_log.id'), index=True)

    arXiv_category_def = relationship('CategoryDef')
    proposal_comment = relationship('AdminLog', primaryjoin='SubmissionCategoryProposal.proposal_comment_id == AdminLog.id')
    response_comment = relationship('AdminLog', primaryjoin='SubmissionCategoryProposal.response_comment_id == AdminLog.id')
    submission = relationship('Submissions')
    user = relationship('TapirUsers')
