from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class EndorsementDomains(Base):
    __tablename__ = 'arXiv_endorsement_domains'


    endorsement_domain = Column(String(32), primary_key=True, server_default=text("''"))
    endorse_all = Column(Enum('y', 'n'), nullable=False, server_default=text("'n'"))
    mods_endorse_all = Column(Enum('y', 'n'), nullable=False, server_default=text("'n'"))
    endorse_email = Column(Enum('y', 'n'), nullable=False, server_default=text("'y'"))
    papers_to_endorse = Column(SMALLINT(5), nullable=False, server_default=text("'4'"))
