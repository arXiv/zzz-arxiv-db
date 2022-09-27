from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class PaperSessions(Base):
    __tablename__ = 'arXiv_paper_sessions'


    paper_session_id = Column(INTEGER(10), primary_key=True)
    paper_id = Column(String(16), nullable=False, server_default=text("''"))
    start_time = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    end_time = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    ip_name = Column(String(16), nullable=False, server_default=text("''"))
