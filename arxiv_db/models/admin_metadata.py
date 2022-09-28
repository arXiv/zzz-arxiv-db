from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class AdminMetadata(Base):
    __tablename__ = 'arXiv_admin_metadata'
    __table_args__ = (
        Index('pidv', 'paper_id', 'version', unique=True),
    )

    metadata_id = Column(INTEGER(11), primary_key=True, index=True)
    document_id = Column(ForeignKey('arXiv_documents.document_id', ondelete='CASCADE'), index=True)
    paper_id = Column(String(64))
    created = Column(DateTime)
    updated = Column(DateTime)
    submitter_name = Column(String(64))
    submitter_email = Column(String(64))
    history = Column(Text)
    source_size = Column(INTEGER(11))
    source_type = Column(String(12))
    title = Column(Text)
    authors = Column(Text)
    category_string = Column(String(255))
    comments = Column(Text)
    proxy = Column(String(255))
    report_num = Column(Text)
    msc_class = Column(String(255))
    acm_class = Column(String(255))
    journal_ref = Column(Text)
    doi = Column(String(255))
    abstract = Column(Text)
    license = Column(String(255))
    version = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    modtime = Column(INTEGER(10))
    is_current = Column(TINYINT(1), server_default=text("'0'"))

    document = relationship('Documents')


t_arXiv_bogus_subject_class = Table(
    'arXiv_bogus_subject_class', metadata,
    Column('document_id', ForeignKey('arXiv_documents.document_id'), nullable=False, index=True, server_default=text("'0'")),
    Column('category_name', String(255), nullable=False, server_default=text("''"))
)
