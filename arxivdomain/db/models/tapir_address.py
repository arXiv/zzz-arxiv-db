from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirAddress(Base):
    __tablename__ = 'tapir_address'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
    address_type = Column(INTEGER(1), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    company = Column(String(80), nullable=False, server_default=text("''"))
    line1 = Column(String(80), nullable=False, server_default=text("''"))
    line2 = Column(String(80), nullable=False, server_default=text("''"))
    city = Column(String(50), nullable=False, index=True, server_default=text("''"))
    state = Column(String(50), nullable=False, server_default=text("''"))
    postal_code = Column(String(16), nullable=False, index=True, server_default=text("''"))
    country = Column(ForeignKey('tapir_countries.digraph'), nullable=False, index=True, server_default=text("''"))
    share_addr = Column(INTEGER(1), nullable=False, server_default=text("'0'"))

    tapir_countries = relationship('TapirCountries')
    user = relationship('TapirUsers')
