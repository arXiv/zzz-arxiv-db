from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class LogPositions(Base):
    __tablename__ = 'arXiv_log_positions'


    id = Column(String(255), primary_key=True, server_default=text("''"))
    position = Column(INTEGER(10))
    date = Column(INTEGER(10))
