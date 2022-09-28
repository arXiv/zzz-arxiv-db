from sqlalchemy import Column, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class SuspectEmails(Base):
    __tablename__ = 'arXiv_suspect_emails'


    id = Column(INTEGER(11), primary_key=True)
    type = Column(String(10), nullable=False)
    pattern = Column(Text, nullable=False)
    comment = Column(Text, nullable=False)
    updated = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
