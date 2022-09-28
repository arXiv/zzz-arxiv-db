from sqlalchemy import Column, String, text

from .. import Base

metadata = Base.metadata


class ArchiveDef(Base):
    __tablename__ = 'arXiv_archive_def'


    archive = Column(String(16), primary_key=True, server_default=text("''"))
    name = Column(String(255))
