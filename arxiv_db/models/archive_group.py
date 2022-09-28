from sqlalchemy import Column, String, text

from .. import Base

metadata = Base.metadata


class ArchiveGroup(Base):
    __tablename__ = 'arXiv_archive_group'


    archive_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    group_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
