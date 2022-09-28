from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class PilotFiles(Base):
    __tablename__ = 'arXiv_pilot_files'

    file_id = Column(INTEGER(11), primary_key=True)
    submission_id = Column(ForeignKey('arXiv_submissions.submission_id'), nullable=False, index=True)
    filename = Column(String(256), server_default=text("''"))
    entity_url = Column(String(256))
    description = Column(String(80))
    byRef = Column(TINYINT(1), server_default=text("'1'"))

    submission = relationship('Submissions')
