from sqlalchemy import CHAR, Column, String, text
from sqlalchemy.dialects.mysql import CHAR, INTEGER

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
