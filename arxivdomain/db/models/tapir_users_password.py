from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirUsersPassword(Base):
    __tablename__ = 'tapir_users_password'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
    password_storage = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    password_enc = Column(String(50), nullable=False, server_default=text("''"))

    user = relationship('TapirUsers', uselist=False)
