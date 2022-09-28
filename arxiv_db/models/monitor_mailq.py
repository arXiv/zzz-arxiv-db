from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class MonitorMailq(Base):
    __tablename__ = 'arXiv_monitor_mailq'


    t = Column(INTEGER(10), primary_key=True, server_default=text("'0'"))
    main_q = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    local_q = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    local_host_map = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    local_timeout = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    local_refused = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    local_in_flight = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
