from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata

class Sessions(Base):
    __tablename__ = 'sessions'


    id = Column(String(72), primary_key=True)
    session_data = Column(Text)
    expires = Column(INTEGER(11))
