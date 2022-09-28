from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class DblpDocumentAuthors(Base):
    __tablename__ = 'arXiv_dblp_document_authors'

    document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, nullable=False, index=True)
    author_id = Column(ForeignKey('arXiv_dblp_authors.author_id'), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    position = Column(TINYINT(4), nullable=False, server_default=text("'0'"))

    author = relationship('DblpAuthors')
    document = relationship('Documents')
