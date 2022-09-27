
class Tracking(Base):
    __tablename__ = 'arXiv_tracking'


    tracking_id = Column(INTEGER(11), primary_key=True)
    sword_id = Column(INTEGER(8), nullable=False, unique=True, server_default=text("'00000000'"))
    paper_id = Column(String(32), nullable=False)
    submission_errors = Column(Text)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata
