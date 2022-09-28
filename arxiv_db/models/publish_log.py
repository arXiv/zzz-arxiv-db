from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class PublishLog(Base):
    __tablename__ = 'arXiv_publish_log'


    date = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
