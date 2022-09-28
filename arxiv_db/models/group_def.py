from sqlalchemy import Column, String, text

from .. import Base

metadata = Base.metadata


class GroupDef(Base):
    __tablename__ = 'arXiv_group_def'


    archive_group = Column(String(16), primary_key=True, server_default=text("''"))
    name = Column(String(255))
