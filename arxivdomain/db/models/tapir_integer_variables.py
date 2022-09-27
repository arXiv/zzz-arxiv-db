from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirIntegerVariables(Base):
    __tablename__ = 'tapir_integer_variables'


    variable_id = Column(String(32), primary_key=True, server_default=text("''"))
    value = Column(INTEGER(4), nullable=False, server_default=text("'0'"))
