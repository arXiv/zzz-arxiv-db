from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Index, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class EndorsementRequests(Base):
    __tablename__ = 'arXiv_endorsement_requests'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
        Index('archive', 'archive', 'subject_class'),
        Index('endorsee_id_2', 'endorsee_id', 'archive', 'subject_class', unique=True)
    )

    request_id = Column(INTEGER(10), primary_key=True)
    endorsee_id = Column(ForeignKey('tapir_users.user_id'), nullable=False, index=True, server_default=text("'0'"))
    archive = Column(String(16), nullable=False, server_default=text("''"))
    subject_class = Column(String(16), nullable=False, server_default=text("''"))
    secret = Column(String(16), nullable=False, unique=True, server_default=text("''"))
    flag_valid = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    issued_when = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    point_value = Column(INTEGER(10), nullable=False, server_default=text("'0'"))

    arXiv_categories = relationship('Categories')
    endorsee = relationship('TapirUsers')
