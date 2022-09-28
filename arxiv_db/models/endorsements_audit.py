from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata

class EndorsementsAudit(Base):
    __tablename__ = 'arXiv_endorsements_audit'

    endorsement_id = Column(ForeignKey('arXiv_endorsements.endorsement_id'), primary_key=True, server_default=text("'0'"))
    session_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    remote_addr = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    flag_knows_personally = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    flag_seen_paper = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    comment = Column(Text)

    endorsement = relationship('Endorsements', uselist=False)
