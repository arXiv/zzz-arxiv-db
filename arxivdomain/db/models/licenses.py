from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class Licenses(Base):
    __tablename__ = 'arXiv_licenses'


    name = Column(String(255), primary_key=True)
    label = Column(String(255))
    active = Column(TINYINT(1), server_default=text("'1'"))
    note = Column(String(255))
    sequence = Column(TINYINT(4))
