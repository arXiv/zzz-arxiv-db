from sqlalchemy import Column, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class TapirAdminAudit(Base):
    __tablename__ = 'tapir_admin_audit'

    log_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    session_id = Column(ForeignKey('tapir_sessions.session_id'), index=True)
    ip_addr = Column(String(16), nullable=False, index=True, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    admin_user = Column(ForeignKey('tapir_users.user_id'), index=True)
    affected_user = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    action = Column(String(32), nullable=False, server_default=text("''"))
    data = Column(Text, nullable=False, index=True)
    comment = Column(Text, nullable=False)
    entry_id = Column(INTEGER(10), primary_key=True)

    tapir_users = relationship('TapirUsers', primaryjoin='TapirAdminAudit.admin_user == TapirUsers.user_id')
    tapir_users1 = relationship('TapirUsers', primaryjoin='TapirAdminAudit.affected_user == TapirUsers.user_id')
    session = relationship('TapirSessions')
