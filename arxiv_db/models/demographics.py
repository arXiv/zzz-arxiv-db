from sqlalchemy import CHAR, Column, Enum, ForeignKey, ForeignKeyConstraint, Index, String, text
from sqlalchemy.dialects.mysql import CHAR, INTEGER, SMALLINT
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata


class Demographics(Base):
    __tablename__ = 'arXiv_demographics'
    __table_args__ = (
        ForeignKeyConstraint(['archive', 'subject_class'], ['arXiv_categories.archive', 'arXiv_categories.subject_class']),
        Index('archive', 'archive', 'subject_class')
    )

    user_id = Column(ForeignKey('tapir_users.user_id'), primary_key=True, server_default=text("'0'"))
    country = Column(CHAR(2), nullable=False, index=True, server_default=text("''"))
    affiliation = Column(String(255), nullable=False, server_default=text("''"))
    url = Column(String(255), nullable=False, server_default=text("''"))
    type = Column(SMALLINT(5), index=True)
    archive = Column(String(16))
    subject_class = Column(String(16))
    original_subject_classes = Column(String(255), nullable=False, server_default=text("''"))
    flag_group_physics = Column(INTEGER(1), index=True)
    flag_group_math = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_group_cs = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_group_nlin = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_proxy = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_journal = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_xml = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    dirty = Column(INTEGER(1), nullable=False, server_default=text("'2'"))
    flag_group_test = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    flag_suspect = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_group_q_bio = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_group_q_fin = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_group_stat = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_group_eess = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_group_econ = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    veto_status = Column(Enum('ok', 'no-endorse', 'no-upload', 'no-replace'), nullable=False, server_default=text("'ok'"))

    arXiv_categories = relationship('Categories')
    user = relationship('TapirUsers', uselist=False, viewonly=True)
