from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class TapirRecoveryTokensUsed(Base):
    __tablename__ = 'tapir_recovery_tokens_used'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
    secret = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    used_when = Column(INTEGER(4))
    used_from = Column(String(16))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    session_id = Column(ForeignKey('tapir_sessions.session_id'), index=True)

    session = relationship('TapirSessions')
    user = relationship('TapirUsers')
