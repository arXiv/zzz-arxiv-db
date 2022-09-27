from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class EndorsementRequestsAudit(Base):
    __tablename__ = 'arXiv_endorsement_requests_audit'

    request_id = Column(ForeignKey('arXiv_endorsement_requests.request_id'), primary_key=True, server_default=text("'0'"))
    session_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    remote_addr = Column(String(16))
    remote_host = Column(String(255))
    tracking_cookie = Column(String(255))

    request = relationship('EndorsementRequests', uselist=False)
