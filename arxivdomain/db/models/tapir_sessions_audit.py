from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirSessionsAudit(Base):
    __tablename__ = 'tapir_sessions_audit'

    session_id = Column(ForeignKey('tapir_sessions.session_id'), primary_key=True, server_default=text("'0'"))
    ip_addr = Column(String(16), nullable=False, index=True, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, index=True, server_default=text("''"))

    session = relationship('TapirSessions', uselist=False)
