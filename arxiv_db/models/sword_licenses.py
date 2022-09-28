from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class SwordLicenses(Base):
    __tablename__ = 'arXiv_sword_licenses'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True)
    license = Column(String(127))
    updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('TapirUsers', uselist=False)
