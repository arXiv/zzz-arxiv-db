from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirPolicyClasses(Base):
    __tablename__ = 'tapir_policy_classes'


    class_id = Column(SMALLINT(5), primary_key=True)
    name = Column(String(64), nullable=False, server_default=text("''"))
    description = Column(Text, nullable=False)
    password_storage = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    recovery_policy = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    permanent_login = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
