from sqlalchemy import Column, Enum, String, text
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class TrackbackSites(Base):
    __tablename__ = 'arXiv_trackback_sites'


    pattern = Column(String(255), nullable=False, index=True, server_default=text("''"))
    site_id = Column(INTEGER(10), primary_key=True)
    action = Column(Enum('neutral', 'accept', 'reject', 'spam'), nullable=False, server_default=text("'neutral'"))
