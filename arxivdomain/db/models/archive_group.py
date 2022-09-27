from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class ArchiveGroup(Base):
    __tablename__ = 'arXiv_archive_group'


    archive_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    group_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
