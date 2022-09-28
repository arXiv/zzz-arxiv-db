from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class TapirEmailHeaders(Base):
    __tablename__ = 'tapir_email_headers'

    template_id = Column(ForeignKey('tapir_email_templates.template_id'), primary_key=True, nullable=False, server_default=text("'0'"))
    header_name = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    header_content = Column(String(255), nullable=False, server_default=text("''"))

    template = relationship('TapirEmailTemplates')
