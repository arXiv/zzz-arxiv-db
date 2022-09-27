from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class Archives(Base):
    __tablename__ = 'arXiv_archives'


    archive_id = Column(String(16), primary_key=True, server_default=text("''"))
    in_group = Column(ForeignKey('arXiv_groups.group_id'), nullable=False, index=True, server_default=text("''"))
    archive_name = Column(String(255), nullable=False, server_default=text("''"))
    start_date = Column(String(4), nullable=False, server_default=text("''"))
    end_date = Column(String(4), nullable=False, server_default=text("''"))
    subdivided = Column(INTEGER(1), nullable=False, server_default=text("'0'"))

    arXiv_groups = relationship('Groups')
