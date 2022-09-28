from sqlalchemy import Column, ForeignKeyConstraint, Index, String, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class CategoryDef(Base):
    __tablename__ = 'arXiv_category_def'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
        Index('cat_def_fk', 'archive', 'subject_class')
    )

    category = Column(String(32), primary_key=True)
    name = Column(String(255))
    active = Column(TINYINT(1), server_default=text("'1'"))
    archive = Column(String(16), nullable=False, server_default=text("''"))
    subject_class = Column(String(16), nullable=False, server_default=text("''"))

    arXiv_categories = relationship('Categories')
