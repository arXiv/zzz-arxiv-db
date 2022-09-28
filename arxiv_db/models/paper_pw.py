from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class PaperPw(Base):
    __tablename__ = 'arXiv_paper_pw'

    document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, server_default=text("'0'"))
    password_storage = Column(INTEGER(1))
    password_enc = Column(String(50))

    document = relationship('Documents', uselist=False)
