from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirCountries(Base):
    __tablename__ = 'tapir_countries'


    digraph = Column(CHAR(2), primary_key=True, server_default=text("''"))
    country_name = Column(String(255), nullable=False, server_default=text("''"))
    rank = Column(INTEGER(1), nullable=False, server_default=text("'255'"))
