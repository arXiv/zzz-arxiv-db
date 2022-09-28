from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import TINYINT

from .. import Base

metadata = Base.metadata


class Licenses(Base):
    __tablename__ = 'arXiv_licenses'


    name = Column(String(255), primary_key=True)
    label = Column(String(255))
    active = Column(TINYINT(1), server_default=text("'1'"))
    note = Column(String(255))
    sequence = Column(TINYINT(4))
