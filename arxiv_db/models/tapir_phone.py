from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class TapirPhone(Base):
    __tablename__ = 'tapir_phone'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, nullable=False, server_default=text("'0'"))
    phone_type = Column(INTEGER(1), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    phone_number = Column(String(32), index=True)
    share_phone = Column(INTEGER(1), nullable=False, server_default=text("'16'"))

    user = relationship('TapirUsers')
