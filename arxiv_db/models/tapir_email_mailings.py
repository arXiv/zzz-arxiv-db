from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class TapirEmailMailings(Base):
    __tablename__ = 'tapir_email_mailings'

    mailing_id = Column(INTEGER(10), primary_key=True)
    template_id = Column(ForeignKey('tapir_email_templates.template_id'), index=True)
    created_by = Column(ForeignKey('tapir_users.user_id'), index=True)
    sent_by = Column(ForeignKey('tapir_users.user_id'), index=True)
    created_date = Column(INTEGER(10))
    sent_date = Column(INTEGER(10))
    complete_date = Column(INTEGER(10))
    mailing_name = Column(String(255))
    comment = Column(Text)

    tapir_users = relationship('TapirUsers', primaryjoin='TapirEmailMailings.created_by == TapirUsers.user_id')
    tapir_users1 = relationship('TapirUsers', primaryjoin='TapirEmailMailings.sent_by == TapirUsers.user_id')
    template = relationship('TapirEmailTemplates')
