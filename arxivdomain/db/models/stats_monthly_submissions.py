from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class StatsMonthlySubmissions(Base):
    __tablename__ = 'arXiv_stats_monthly_submissions'


    ym = Column(Date, primary_key=True, server_default=text("'0000-00-00'"))
    num_submissions = Column(SMALLINT(5), nullable=False)
    historical_delta = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
