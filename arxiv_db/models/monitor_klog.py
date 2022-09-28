from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class MonitorKlog(Base):
    __tablename__ = 'arXiv_monitor_klog'


    t = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
    sent = Column(INTEGER(10))
