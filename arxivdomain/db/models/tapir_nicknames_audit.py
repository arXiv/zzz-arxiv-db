from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirNicknamesAudit(Base):
    __tablename__ = 'tapir_nicknames_audit'


    nick_id = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
    creation_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    creation_ip_num = Column(String(16), nullable=False, index=True, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, index=True, server_default=text("''"))
