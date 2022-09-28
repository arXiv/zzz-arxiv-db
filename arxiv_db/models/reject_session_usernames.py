from sqlalchemy import Column, String, text

from .. import Base

metadata = Base.metadata


class RejectSessionUsernames(Base):
    __tablename__ = 'arXiv_reject_session_usernames'


    username = Column(String(64), primary_key=True, server_default=text("''"))
