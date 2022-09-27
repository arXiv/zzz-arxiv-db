from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TrackbackSites(Base):
    __tablename__ = 'arXiv_trackback_sites'


    pattern = Column(String(255), nullable=False, index=True, server_default=text("''"))
    site_id = Column(INTEGER(10), primary_key=True)
    action = Column(Enum('neutral', 'accept', 'reject', 'spam'), nullable=False, server_default=text("'neutral'"))
