from sqlalchemy import Column, Enum, ForeignKey, ForeignKeyConstraint, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class CrossControl(Base):
    __tablename__ = 'arXiv_cross_control'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
        Index('archive', 'archive', 'subject_class'),
        Index('document_id', 'document_id', 'version')
    )

    control_id = Column(INTEGER(10), primary_key=True)
    document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, server_default=text("'0'"))
    version = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    desired_order = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    status = Column(Enum('new', 'frozen', 'published', 'rejected'), nullable=False, index=True, server_default=text("'new'"))
    flag_must_notify = Column(Enum('0', '1'), server_default=text("'1'"))
    archive = Column(String(16), nullable=False, server_default=text("''"))
    subject_class = Column(String(16), nullable=False, server_default=text("''"))
    request_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    freeze_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    publish_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))

    arXiv_categories = relationship('Categories')
    document = relationship('Documents')
    user = relationship('TapirUsers')
