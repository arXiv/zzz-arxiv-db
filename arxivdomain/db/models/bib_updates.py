from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class BibUpdates(Base):
    __tablename__ = 'arXiv_bib_updates'


    update_id = Column(MEDIUMINT(8), primary_key=True)
    document_id = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    bib_id = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    journal_ref = Column(Text)
    doi = Column(Text)
