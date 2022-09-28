from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class QueueView(Base):
    __tablename__ = 'arXiv_queue_view'

    user_id = Column(ForeignKey('tapir_users.user_id', ondelete='CASCADE'), primary_key=True, server_default=text("'0'"))
    last_view = Column(DateTime)
    second_last_view = Column(DateTime)
    total_views = Column(INTEGER(3), nullable=False, server_default=text("'0'"))

    user = relationship('TapirUsers', uselist=False)
