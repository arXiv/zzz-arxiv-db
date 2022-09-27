from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class NextMail(Base):
    __tablename__ = 'arXiv_next_mail'

    __table_args__ = (
        Index('arXiv_next_mail_idx_document_id_version', 'document_id', 'version'),
    )

    next_mail_id = Column(INTEGER(11), primary_key=True)
    submission_id = Column(INTEGER(11), nullable=False)
    document_id = Column(MEDIUMINT(8), nullable=False, index=True, server_default=text("'0'"))
    paper_id = Column(String(20))
    version = Column(INTEGER(4), nullable=False, server_default=text("'1'"))
    type = Column(String(255), nullable=False, server_default=text("'new'"))
    extra = Column(String(255))
    mail_id = Column(CHAR(6))
    is_written = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
