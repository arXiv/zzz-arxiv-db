from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class Dblp(Base):
    __tablename__ = 'arXiv_dblp'

    document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, server_default=text("'0'"))
    url = Column(String(80))

    document = relationship('Documents', uselist=False)
