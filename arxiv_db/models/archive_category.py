from sqlalchemy import Column, String, text

from .. import Base

metadata = Base.metadata


class ArchiveCategory(Base):
    __tablename__ = 'arXiv_archive_category'


    archive_id = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    category_id = Column(String(32), primary_key=True, nullable=False)
