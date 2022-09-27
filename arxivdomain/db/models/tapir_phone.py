from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirPhone(Base):
    __tablename__ = 'tapir_phone'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
    phone_type = Column(INTEGER(1), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    phone_number = Column(String(32), index=True)
    share_phone = Column(INTEGER(1), nullable=False, server_default=text("'16'"))

    user = relationship('TapirUsers')
