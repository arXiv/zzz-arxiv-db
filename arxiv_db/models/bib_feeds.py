from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMINT, TINYINT

from .. import Base

metadata = Base.metadata


class BibFeeds(Base):
    __tablename__ = 'arXiv_bib_feeds'


    bib_id = Column(MEDIUMINT(8), primary_key=True)
    name = Column(String(64), nullable=False, server_default=text("''"))
    priority = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    uri = Column(String(255))
    identifier = Column(String(255))
    version = Column(String(255))
    strip_journal_ref = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    concatenate_dupes = Column(INTEGER(11))
    max_updates = Column(INTEGER(11))
    email_errors = Column(String(255))
    prune_ids = Column(Text)
    prune_regex = Column(Text)
    enabled = Column(TINYINT(1), server_default=text("'0'"))
