from sqlalchemy import Column, String, text

from .. import Base

metadata = Base.metadata


class Groups(Base):
    __tablename__ = 'arXiv_groups'


    group_id = Column(String(16), primary_key=True, server_default=text("''"))
    group_name = Column(String(255), nullable=False, server_default=text("''"))
    start_year = Column(String(4), nullable=False, server_default=text("''"))
