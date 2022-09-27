from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirEmailLog(Base):
    __tablename__ = 'tapir_email_log'


    mail_id = Column(INTEGER(10), primary_key=True)
    reference_type = Column(CHAR(1))
    reference_id = Column(INTEGER(4))
    sent_date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    email = Column(String(50), nullable=False, server_default=text("''"))
    flag_bounced = Column(INTEGER(1))
    mailing_id = Column(INTEGER(10), index=True)
    template_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
