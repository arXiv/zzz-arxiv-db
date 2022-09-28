from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class SuspiciousNames(Base):
    __tablename__ = 'arXiv_suspicious_names'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
    full_name = Column(String(255), nullable=False, server_default=text("''"))

    user = relationship('TapirUsers', uselist=False)
