from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class MirrorList(Base):
    __tablename__ = 'arXiv_mirror_list'

    mirror_list_id = Column(INTEGER(11), primary_key=True)
    created = Column(DateTime)
    updated = Column(DateTime)
    document_id = Column(ForeignKey('arXiv_documents.document_id'), nullable=False, index=True, server_default=text("'0'"))
    version = Column(INTEGER(4), nullable=False, server_default=text("'1'"))
    write_source = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    write_abs = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    is_written = Column(TINYINT(1), nullable=False, server_default=text("'0'"))

    document = relationship('Documents')
