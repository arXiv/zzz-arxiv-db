from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class SubscriptionUniversalInstitution(Base):
    __tablename__ = 'Subscription_UniversalInstitution'


    resolver_URL = Column(String(255))
    name = Column(String(255), nullable=False, index=True)
    label = Column(String(255))
    id = Column(INTEGER(11), primary_key=True)
    alt_text = Column(String(255))
    link_icon = Column(String(255))
    note = Column(String(255))
