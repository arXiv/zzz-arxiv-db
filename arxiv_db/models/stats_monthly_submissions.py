from sqlalchemy import Column, Date, text
from sqlalchemy.dialects.mysql import SMALLINT, TINYINT

from .. import Base

metadata = Base.metadata


class StatsMonthlySubmissions(Base):
    __tablename__ = 'arXiv_stats_monthly_submissions'


    ym = Column(Date, primary_key=True, server_default=text("'0000-00-00'"))
    num_submissions = Column(SMALLINT(5), nullable=False)
    historical_delta = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
