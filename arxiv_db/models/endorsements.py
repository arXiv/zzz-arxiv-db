from sqlalchemy import Column, Enum, ForeignKey, ForeignKeyConstraint, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class Endorsements(Base):
    __tablename__ = 'arXiv_endorsements'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
        Index('endorser_id_2', 'endorser_id', 'endorsee_id', 'archive', 'subject_class', unique=True),
        Index('archive', 'archive', 'subject_class')
    )

    endorsement_id = Column(INTEGER(10), primary_key=True)
    endorser_id = Column(ForeignKey('tapir_users.user_id'), index=True)
    endorsee_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    archive = Column(String(16), nullable=False, server_default=text("''"))
    subject_class = Column(String(16), nullable=False, server_default=text("''"))
    flag_valid = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    type = Column(Enum('user', 'admin', 'auto'))
    point_value = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    issued_when = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    request_id = Column(ForeignKey('arXiv_endorsement_requests.request_id'), index=True)

    arXiv_categories = relationship('Categories')
    endorsee = relationship('TapirUsers', primaryjoin='Endorsements.endorsee_id == TapirUsers.user_id')
    endorser = relationship('TapirUsers', primaryjoin='Endorsements.endorser_id == TapirUsers.user_id')
    request = relationship('EndorsementRequests')
