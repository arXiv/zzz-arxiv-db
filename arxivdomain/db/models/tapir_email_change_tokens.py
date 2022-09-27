from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirEmailChangeTokens(Base):
    __tablename__ = 'tapir_email_change_tokens'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
    old_email = Column(String(50), nullable=False, server_default=text("''"))
    new_email = Column(String(50), nullable=False, server_default=text("''"))
    secret = Column(String(32), primary_key=True, nullable=False, index=True, server_default=text("''"))
    tapir_dest = Column(String(255), nullable=False, server_default=text("''"))
    issued_when = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    issued_to = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(16), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    used = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    session_id = Column(INTEGER(4), nullable=False, server_default=text("'0'"))
    consumed_when = Column(INTEGER(10))
    consumed_from = Column(String(16))

    user = relationship('TapirUsers')
