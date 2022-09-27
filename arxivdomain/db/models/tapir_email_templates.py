from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirEmailTemplates(Base):
    __tablename__ = 'tapir_email_templates'
    __table_args__ = (
        Index('short_name', 'short_name', 'lang', unique=True),
    )

    template_id = Column(INTEGER(10), primary_key=True)
    short_name = Column(String(32), nullable=False, server_default=text("''"))
    lang = Column(CHAR(2), nullable=False, server_default=text("'en'"))
    long_name = Column(String(255), nullable=False, server_default=text("''"))
    data = Column(Text, nullable=False)
    sql_statement = Column(Text, nullable=False)
    update_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    created_by = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    updated_by = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    workflow_status = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    flag_system = Column(INTEGER(1), nullable=False, server_default=text("'0'"))

    tapir_users = relationship('TapirUsers', primaryjoin='TapirEmailTemplates.created_by == TapirUsers.user_id')
    tapir_users1 = relationship('TapirUsers', primaryjoin='TapirEmailTemplates.updated_by == TapirUsers.user_id')
