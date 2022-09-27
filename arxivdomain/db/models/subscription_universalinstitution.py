from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class SubscriptionUniversalInstitution(Base):
    __tablename__ = 'Subscription_UniversalInstitution'


    resolver_URL = Column(String(255))
    name = Column(String(255), nullable=False, index=True)
    label = Column(String(255))
    id = Column(INTEGER(11), primary_key=True)
    alt_text = Column(String(255))
    link_icon = Column(String(255))
    note = Column(String(255))
