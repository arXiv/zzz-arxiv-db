from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class Groups(Base):
    __tablename__ = 'arXiv_groups'


    group_id = Column(String(16), primary_key=True, server_default=text("''"))
    group_name = Column(String(255), nullable=False, server_default=text("''"))
    start_year = Column(String(4), nullable=False, server_default=text("''"))
