from sqlalchemy import Column, ForeignKey, Index, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class SubscriptionUniversalInstitutionIP(Base):
    __tablename__ = 'Subscription_UniversalInstitutionIP'

    __table_args__ = (
        Index('ip', 'start', 'end'),
    )

    sid = Column(ForeignKey('Subscription_UniversalInstitution.id', ondelete='CASCADE'), nullable=False, index=True)
    id = Column(INTEGER(11), primary_key=True)
    exclude = Column(TINYINT(4), server_default=text("'0'"))
    end = Column(BIGINT(20), nullable=False, index=True)
    start = Column(BIGINT(20), nullable=False, index=True)

    Subscription_UniversalInstitution = relationship('SubscriptionUniversalInstitution')
