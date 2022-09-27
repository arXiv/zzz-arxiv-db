from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class AwsConfig(Base):
    __tablename__ = 'arXiv_aws_config'


    domain = Column(String(75), primary_key=True, nullable=False)
    keyname = Column(String(60), primary_key=True, nullable=False)
    value = Column(String(150))
