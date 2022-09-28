from sqlalchemy import Column, Enum, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, TINYINT

from .. import Base

metadata = Base.metadata


class TrackbackPings(Base):
    __tablename__ = 'arXiv_trackback_pings'


    trackback_id = Column(MEDIUMINT(8), primary_key=True)
    document_id = Column(MEDIUMINT(8), index=True)
    title = Column(String(255), nullable=False, server_default=text("''"))
    excerpt = Column(String(255), nullable=False, server_default=text("''"))
    url = Column(String(255), nullable=False, index=True, server_default=text("''"))
    blog_name = Column(String(255), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    remote_addr = Column(String(16), nullable=False, server_default=text("''"))
    posted_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    is_stale = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    approved_by_user = Column(MEDIUMINT(9), nullable=False, server_default=text("'0'"))
    approved_time = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    status = Column(Enum('pending', 'pending2', 'accepted', 'rejected', 'spam'), nullable=False, index=True, server_default=text("'pending'"))
    site_id = Column(INTEGER(10))

