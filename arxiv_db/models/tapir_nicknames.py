from sqlalchemy import Column, ForeignKey, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class TapirNicknames(Base):
    __tablename__ = 'tapir_nicknames'
    __table_args__ = (
        Index('user_id', 'user_id', 'user_seq', unique=True),
    )

    nick_id = Column(INTEGER(10), primary_key=True)
    nickname = Column(String(20), nullable=False, unique=True, server_default=text("''"))
    user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, server_default=text("'0'"))
    user_seq = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    flag_valid = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    role = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    policy = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    flag_primary = Column(INTEGER(1), nullable=False, server_default=text("'0'"))

    user = relationship('TapirUsers')
