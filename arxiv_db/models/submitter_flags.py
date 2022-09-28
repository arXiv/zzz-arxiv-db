from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class SubmitterFlags(Base):
    __tablename__ = 'arXiv_submitter_flags'


    flag_id = Column(INTEGER(11), primary_key=True)
    comment = Column(String(255))
    pattern = Column(String(255))
