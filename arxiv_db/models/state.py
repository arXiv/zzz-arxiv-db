from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class State(Base):
    __tablename__ = 'arXiv_state'


    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(24))
    value = Column(String(24))
