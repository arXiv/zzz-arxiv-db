from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class LogPositions(Base):
    __tablename__ = 'arXiv_log_positions'


    id = Column(String(255), primary_key=True, server_default=text("''"))
    position = Column(INTEGER(10))
    date = Column(INTEGER(10))
