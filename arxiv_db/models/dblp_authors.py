from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import MEDIUMINT

from .. import Base

metadata = Base.metadata


class DblpAuthors(Base):
    __tablename__ = 'arXiv_dblp_authors'


    author_id = Column(MEDIUMINT(8), primary_key=True, unique=True)
    name = Column(String(40), unique=True)
