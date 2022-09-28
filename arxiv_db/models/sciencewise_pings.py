from sqlalchemy import Column, DateTime, String

from .. import Base

metadata = Base.metadata


class SciencewisePings(Base):
    __tablename__ = 'arXiv_sciencewise_pings'


    paper_id_v = Column(String(32), primary_key=True)
    updated = Column(DateTime)
