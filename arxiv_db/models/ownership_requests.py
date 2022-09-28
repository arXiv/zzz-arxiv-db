from sqlalchemy import Column, Enum, ForeignKey, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class OwnershipRequests(Base):
    __tablename__ = 'arXiv_ownership_requests'

    request_id = Column(INTEGER(10), primary_key=True)
    user_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    endorsement_request_id = Column(ForeignKey('arXiv_endorsement_requests.request_id'), index=True)
    workflow_status = Column(Enum('pending', 'accepted', 'rejected'), nullable=False, server_default=text("'pending'"))

    endorsement_request = relationship('EndorsementRequests')
    user = relationship('TapirUsers')
