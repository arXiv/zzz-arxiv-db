from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class PaperSessions(Base):
    __tablename__ = 'arXiv_paper_sessions'


    paper_session_id = Column(INTEGER(10), primary_key=True)
    paper_id = Column(String(16), nullable=False, server_default=text("''"))
    start_time = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    end_time = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    ip_name = Column(String(16), nullable=False, server_default=text("''"))
