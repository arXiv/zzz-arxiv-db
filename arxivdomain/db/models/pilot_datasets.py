from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class PilotDatasets(Base):
    __tablename__ = 'arXiv_pilot_datasets'

    submission_id = Column(ForeignKey('arXiv_submissions.submission_id'), primary_key=True)
    numfiles = Column(SMALLINT(4), server_default=text("'0'"))
    feed_url = Column(String(256))
    manifestation = Column(String(256))
    published = Column(TINYINT(1), server_default=text("'0'"))
    created = Column(DateTime, nullable=False)
    last_checked = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    submission = relationship('Submissions', uselist=False)
