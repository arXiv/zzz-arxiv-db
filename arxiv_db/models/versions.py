from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class Versions(Base):
    __tablename__ = 'arXiv_versions'

    document_id = Column(ForeignKey('arXiv_documents.document_id'), primary_key=True, nullable=False, server_default=text("'0'"))
    version = Column(TINYINT(3), primary_key=True, nullable=False, server_default=text("'0'"))
    request_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    freeze_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    publish_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    flag_current = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))

    document = relationship('Documents')
