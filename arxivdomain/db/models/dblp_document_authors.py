from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class DblpDocumentAuthors(Base):
    __tablename__ = 'arXiv_dblp_document_authors'

    document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, nullable=False, index=True)
    author_id = Column(ForeignKey('arXiv_dblp_authors.author_id'), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    position = Column(TINYINT(4), nullable=False, server_default=text("'0'"))

    author = relationship('DblpAuthors')
    document = relationship('Documents')
