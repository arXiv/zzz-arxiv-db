from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class Versions(Base):
    __tablename__ = 'arXiv_versions'

    document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, nullable=False, server_default=text("'0'"))
    version = Column(TINYINT(3), primary_key=True, nullable=False, server_default=text("'0'"))
    request_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    freeze_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    publish_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    flag_current = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))

    document = relationship('Documents')
