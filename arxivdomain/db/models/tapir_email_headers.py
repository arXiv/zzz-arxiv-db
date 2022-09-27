from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirEmailHeaders(Base):
    __tablename__ = 'tapir_email_headers'

    template_id = Column(ForeignKey('tapir_email_templates.template_id'), primary_key=True, nullable=False, server_default=text("'0'"))
    header_name = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    header_content = Column(String(255), nullable=False, server_default=text("''"))

    template = relationship('TapirEmailTemplates')
