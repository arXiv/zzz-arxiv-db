from sqlalchemy import Column, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class Documents(Base):
    __tablename__ = 'arXiv_documents'


    document_id = Column(MEDIUMINT(8), primary_key=True)
    paper_id = Column(String(20), nullable=False, unique=True, server_default=text("''"))
    title = Column(String(255), nullable=False, index=True, server_default=text("''"))
    authors = Column(Text)
    submitter_email = Column(String(64), nullable=False, index=True, server_default=text("''"))
    submitter_id = Column(ForeignKey('tapir_users.user_id'), index=True)
    dated = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    primary_subject_class = Column(String(16))
    created = Column(DateTime)

    submitter = relationship('TapirUsers')
