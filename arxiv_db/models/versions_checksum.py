from sqlalchemy import BINARY, Column, ForeignKeyConstraint, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class VersionsChecksum(Base):
    __tablename__ = 'arXiv_versions_checksum'
    __table_args__ = (
        ForeignKeyConstraint(['document_id', 'version'], ['arXiv_versions.document_id', 'arXiv_versions.version']),
    )

    document_id = Column(MEDIUMINT(8), primary_key=True, nullable=False, server_default=text("'0'"))
    version = Column(TINYINT(3), primary_key=True, nullable=False, server_default=text("'0'"))
    flag_abs_present = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    abs_size = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    abs_md5sum = Column(BINARY(16), index=True)
    flag_src_present = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    src_size = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    src_md5sum = Column(BINARY(16), index=True)

    document = relationship('Versions', uselist=False)
