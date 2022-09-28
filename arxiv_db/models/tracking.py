from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class Tracking(Base):
    __tablename__ = 'arXiv_tracking'


    tracking_id = Column(INTEGER(11), primary_key=True)
    sword_id = Column(INTEGER(8), nullable=False, unique=True, server_default=text("'00000000'"))
    paper_id = Column(String(32), nullable=False)
    submission_errors = Column(Text)
    timestamp = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
