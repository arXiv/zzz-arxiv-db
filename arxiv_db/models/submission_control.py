from sqlalchemy import Column, Enum, ForeignKey, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class SubmissionControl(Base):
    __tablename__ = 'arXiv_submission_control'
    __table_args__ = (
        Index('document_id', 'document_id', 'version', unique=True),
    )

    control_id = Column(INTEGER(10), primary_key=True)
    document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, server_default=text("'0'"))
    version = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    pending_paper_id = Column(String(20), nullable=False, index=True, server_default=text("''"))
    user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    status = Column(Enum('new', 'frozen', 'published', 'rejected'), nullable=False, index=True, server_default=text("'new'"))
    flag_must_notify = Column(Enum('0', '1'), server_default=text("'1'"))
    request_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    freeze_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    publish_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))

    document = relationship('Documents')
    user = relationship('TapirUsers')
