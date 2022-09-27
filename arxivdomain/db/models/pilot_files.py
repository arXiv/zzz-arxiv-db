from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class PilotFiles(Base):
    __tablename__ = 'arXiv_pilot_files'

    file_id = Column(INTEGER(11), primary_key=True)
    submission_id = Column(ForeignKey('arXiv_submissions.submission_id'), nullable=False, index=True)
    filename = Column(String(256), server_default=text("''"))
    entity_url = Column(String(256))
    description = Column(String(80))
    byRef = Column(TINYINT(1), server_default=text("'1'"))

    submission = relationship('Submissions')
