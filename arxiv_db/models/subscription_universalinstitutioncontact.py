from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class SubscriptionUniversalInstitutionContact(Base):
    __tablename__ = 'Subscription_UniversalInstitutionContact'


    email = Column(String(255))
    sid = Column(ForeignKey('Subscription_UniversalInstitution.id', ondelete='CASCADE'), nullable=False, index=True)
    active = Column(TINYINT(4), server_default=text("'0'"))
    contact_name = Column(String(255))
    id = Column(INTEGER(11), primary_key=True)
    phone = Column(String(255))
    note = Column(String(2048))

    Subscription_UniversalInstitution = relationship('SubscriptionUniversalInstitution')
