from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class TapirSessionsAudit(Base):
    __tablename__ = 'tapir_sessions_audit'

    session_id = Column(ForeignKey('tapir_sessions.session_id'), primary_key=True, server_default=text("'0'"))
    ip_addr = Column(String(16), nullable=False, index=True, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, index=True, server_default=text("''"))

    session = relationship('TapirSessions', uselist=False)
