from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class OrcidIds(Base):
    __tablename__ = 'arXiv_orcid_ids'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True)
    orcid = Column(String(19), nullable=False, index=True)
    authenticated = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('TapirUsers', uselist=False)
