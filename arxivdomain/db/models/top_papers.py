from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TopPapers(Base):
    __tablename__ = 'arXiv_top_papers'

    from_week = Column(Date, primary_key=True, nullable=False, server_default=text("'0000-00-00'"))
    _class = Column('class', CHAR(1), primary_key=True, nullable=False, server_default=text("''"))
    rank = Column(SMALLINT(5), primary_key=True, nullable=False, server_default=text("'0'"))
    document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, index=True, server_default=text("'0'"))
    viewers = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))

    document = relationship('Documents')
