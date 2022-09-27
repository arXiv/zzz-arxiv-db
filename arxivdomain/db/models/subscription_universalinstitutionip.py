from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class SubscriptionUniversalInstitutionIP(Base):
    __tablename__ = 'Subscription_UniversalInstitutionIP'

    __table_args__ = (
        Index('ip', 'start', 'end'),
    )

    sid = Column(ForeignKey('Subscription_UniversalInstitution.id', ondelete='CASCADE'), nullable=False, index=True)
    id = Column(INTEGER(11), primary_key=True)
    exclude = Column(TINYINT(4), server_default=text("'0'"))
    end = Column(BIGINT(20), nullable=False, index=True)
    start = Column(BIGINT(20), nullable=False, index=True)

    Subscription_UniversalInstitution = relationship('SubscriptionUniversalInstitution')
