from sqlalchemy import Column, DateTime, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import SMALLINT, TINYINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class PilotDatasets(Base):
    __tablename__ = 'arXiv_pilot_datasets'

    submission_id = Column(ForeignKey('arXiv_submissions.submission_id'), primary_key=True)
    numfiles = Column(SMALLINT(4), server_default=text("'0'"))
    feed_url = Column(String(256))
    manifestation = Column(String(256))
    published = Column(TINYINT(1), server_default=text("'0'"))
    created = Column(DateTime, nullable=False)
    last_checked = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    submission = relationship('Submissions', uselist=False)
