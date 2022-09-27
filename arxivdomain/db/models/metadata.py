from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class Metadata(Base):
    __tablename__ = 'arXiv_metadata'
    __table_args__ = (
        Index('pidv', 'paper_id', 'version', unique=True),
    )

    metadata_id = Column(INTEGER(11), primary_key=True)
    document_id = Column(ForeignKey('arXiv_documents.document_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'0'"))
    paper_id = Column(String(64), nullable=False)
    created = Column(DateTime)
    updated = Column(DateTime)
    submitter_id = Column(ForeignKey('tapir_users.user_id'), index=True)
    submitter_name = Column(String(64), nullable=False)
    submitter_email = Column(String(64), nullable=False)
    source_size = Column(INTEGER(11))
    source_format = Column(String(12))
    source_flags = Column(String(12))
    title = Column(Text)
    authors = Column(Text)
    abs_categories = Column(String(255))
    comments = Column(Text)
    proxy = Column(String(255))
    report_num = Column(Text)
    msc_class = Column(String(255))
    acm_class = Column(String(255))
    journal_ref = Column(Text)
    doi = Column(String(255))
    abstract = Column(Text)
    license = Column(ForeignKey('arXiv_licenses.name'), index=True)
    version = Column(INTEGER(4), nullable=False, server_default=text("'1'"))
    modtime = Column(INTEGER(11))
    is_current = Column(TINYINT(1), server_default=text("'1'"))
    is_withdrawn = Column(TINYINT(1), nullable=False, server_default=text("'0'"))

    document = relationship('Documents')
    arXiv_licenses = relationship('Licenses')
    submitter = relationship('TapirUsers')
