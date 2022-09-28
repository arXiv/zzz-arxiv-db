from sqlalchemy import Column, ForeignKeyConstraint, String, text
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class QuestionableCategories(Base):
    __tablename__ = 'arXiv_questionable_categories'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
    )

    archive = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))
    subject_class = Column(String(16), primary_key=True, nullable=False, server_default=text("''"))

    arXiv_categories = relationship('Categories', uselist=False)
