from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class OwnershipRequestsAudit(Base):
    __tablename__ = 'arXiv_ownership_requests_audit'

    request_id = Column(ForeignKey('arXiv_ownership_requests.request_id'), primary_key=True, server_default=text("'0'"))
    session_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    remote_addr = Column(String(16), nullable=False, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    date = Column(INTEGER(10), nullable=False, server_default=text("'0'"))

    request = relationship('OwnershipRequests', uselist=False)
