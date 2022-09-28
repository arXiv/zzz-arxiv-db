from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class TapirNicknamesAudit(Base):
    __tablename__ = 'tapir_nicknames_audit'


    nick_id = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
    creation_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    creation_ip_num = Column(String(16), nullable=False, index=True, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, index=True, server_default=text("''"))
