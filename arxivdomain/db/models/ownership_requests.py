from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class OwnershipRequests(Base):
    __tablename__ = 'arXiv_ownership_requests'

    request_id = Column(INTEGER(10), primary_key=True)
    user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    endorsement_request_id = Column(ForeignKey('arXiv_endorsement_requests.request_id'), index=True)
    workflow_status = Column(Enum('pending', 'accepted', 'rejected'), nullable=False, server_default=text("'pending'"))

    endorsement_request = relationship('EndorsementRequests')
    user = relationship('TapirUsers')
