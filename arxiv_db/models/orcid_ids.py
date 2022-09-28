from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class OrcidIds(Base):
    __tablename__ = 'arXiv_orcid_ids'

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True)
    orcid = Column(String(19), nullable=False, index=True)
    authenticated = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('TapirUsers', uselist=False)
