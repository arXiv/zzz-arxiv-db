from sqlalchemy import Column, Date
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class StatsMonthlyDownloads(Base):
    __tablename__ = 'arXiv_stats_monthly_downloads'


    ym = Column(Date, primary_key=True)
    downloads = Column(INTEGER(10), nullable=False)
