from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class Dblp(Base):
    __tablename__ = 'arXiv_dblp'

    document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, server_default=text("'0'"))
    url = Column(String(80))

    document = relationship('Documents', uselist=False)
