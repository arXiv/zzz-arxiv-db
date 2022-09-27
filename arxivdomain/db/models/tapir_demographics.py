from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirDemographics(Base):
    __tablename__ = 'tapir_demographics'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
    gender = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    share_gender = Column(INTEGER(1), nullable=False, server_default=text("'16'"))
    birthday = Column(Date, index=True)
    share_birthday = Column(INTEGER(1), nullable=False, server_default=text("'16'"))
    country = Column(ForeignKey('tapir_countries.digraph'), nullable=False, index=True, server_default=text("''"))
    share_country = Column(INTEGER(1), nullable=False, server_default=text("'16'"))
    postal_code = Column(String(16), nullable=False, index=True, server_default=text("''"))

    tapir_countries = relationship('TapirCountries')
    user = relationship('TapirUsers', uselist=False)
