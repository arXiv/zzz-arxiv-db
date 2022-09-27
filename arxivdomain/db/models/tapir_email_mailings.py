from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirEmailMailings(Base):
    __tablename__ = 'tapir_email_mailings'

    mailing_id = Column(INTEGER(10), primary_key=True)
    template_id = Column(ForeignKey('tapir_email_templates.template_id'), index=True)
    created_by = Column(ForeignKey('tapir_users.user_id'), index=True)
    sent_by = Column(ForeignKey('tapir_users.user_id'), index=True)
    created_date = Column(INTEGER(10))
    sent_date = Column(INTEGER(10))
    complete_date = Column(INTEGER(10))
    mailing_name = Column(String(255))
    comment = Column(Text)

    tapir_users = relationship('TapirUsers', primaryjoin='TapirEmailMailings.created_by == TapirUsers.user_id')
    tapir_users1 = relationship('TapirUsers', primaryjoin='TapirEmailMailings.sent_by == TapirUsers.user_id')
    template = relationship('TapirEmailTemplates')
