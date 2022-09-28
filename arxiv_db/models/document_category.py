from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class DocumentCategory(Base):
    __tablename__ = 'arXiv_document_category'

    document_id = Column(ForeignKey('arXiv_documents.document_id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True, server_default=text("'0'"))
    category = Column(ForeignKey('arXiv_category_def.category'), primary_key=True, nullable=False, index=True)
    is_primary = Column(TINYINT(1), nullable=False, server_default=text("'0'"))

    arXiv_category_def = relationship('CategoryDef')
    document = relationship('Documents')
