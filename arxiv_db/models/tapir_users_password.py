from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class TapirUsersPassword(Base):
    __tablename__ = 'tapir_users_password'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
    password_storage = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    password_enc = Column(String(50), nullable=False, server_default=text("''"))

    user = relationship('TapirUsers', uselist=False)
