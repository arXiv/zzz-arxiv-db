from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class AdminLog(Base):
    __tablename__ = 'arXiv_admin_log'


    id = Column(INTEGER(11), primary_key=True)
    logtime = Column(String(24))
    created = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    paper_id = Column(String(20), index=True)
    username = Column(String(20), index=True)
    host = Column(String(64))
    program = Column(String(20))
    command = Column(String(20), index=True)
    logtext = Column(Text)
    document_id = Column(MEDIUMINT(8))
    submission_id = Column(INTEGER(11), index=True)
    notify = Column(TINYINT(1), server_default=text("'0'"))
