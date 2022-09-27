from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class SuspiciousNames(Base):
    __tablename__ = 'arXiv_suspicious_names'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
    full_name = Column(String(255), nullable=False, server_default=text("''"))

    user = relationship('TapirUsers', uselist=False)
