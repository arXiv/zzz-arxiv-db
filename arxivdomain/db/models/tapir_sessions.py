from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirSessions(Base):
    __tablename__ = 'tapir_sessions'

    session_id = Column(INTEGER(4), primary_key=True)
    user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    last_reissue = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    start_time = Column(INTEGER(11), nullable=False, index=True, server_default=text("'0'"))
    end_time = Column(INTEGER(11), nullable=False, index=True, server_default=text("'0'"))

    user = relationship('TapirUsers')
