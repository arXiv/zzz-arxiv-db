from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class AuthorIds(Base):
    __tablename__ = 'arXiv_author_ids'


    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True)
    author_id = Column(String(50), nullable=False, index=True)
    updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('TapirUsers', uselist=False)
