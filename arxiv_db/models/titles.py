from sqlalchemy import Column, Date, String

from .. import Base

metadata = Base.metadata


class Titles(Base):
    __tablename__ = 'arXiv_titles'


    paper_id = Column(String(64), primary_key=True)
    title = Column(String(255), index=True)
    report_num = Column(String(255), index=True)
    date = Column(Date)
