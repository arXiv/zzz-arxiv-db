from sqlalchemy import Column, ForeignKey, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class ShowEmailRequests(Base):
    __tablename__ = 'arXiv_show_email_requests'
    __table_args__ = (
        Index('user_id', 'user_id', 'dated'),
    )

    document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, index=True, server_default=text("'0'"))
    user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, server_default=text("'0'"))
    session_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    dated = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    flag_allowed = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    remote_addr = Column(String(16), nullable=False, index=True, server_default=text("''"))
    remote_host = Column(String(255), nullable=False, server_default=text("''"))
    tracking_cookie = Column(String(255), nullable=False, server_default=text("''"))
    request_id = Column(INTEGER(10), primary_key=True)

    document = relationship('Documents')
    user = relationship('TapirUsers')
