from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class TapirUsersHot(Base):
    __tablename__ = 'tapir_users_hot'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
    last_login = Column(INTEGER(4), nullable=False, index=True, server_default=text("'0'"))
    second_last_login = Column(INTEGER(4), nullable=False, index=True, server_default=text("'0'"))
    number_sessions = Column(INTEGER(4), nullable=False, index=True, server_default=text("'0'"))

    user = relationship('TapirUsers', uselist=False)
