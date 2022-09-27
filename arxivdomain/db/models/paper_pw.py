from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class PaperPw(Base):
    __tablename__ = 'arXiv_paper_pw'

    document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, server_default=text("'0'"))
    password_storage = Column(INTEGER(1))
    password_enc = Column(String(50))

    document = relationship('Documents', uselist=False)
