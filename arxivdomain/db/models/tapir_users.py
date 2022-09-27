from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class TapirUsers(Base):
    __tablename__ = 'tapir_users'


    user_id = Column(INTEGER(4), primary_key=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    suffix_name = Column(String(50))
    share_first_name = Column(INTEGER(1), nullable=False, server_default=text("'1'"))
    share_last_name = Column(INTEGER(1), nullable=False, server_default=text("'1'"))
    email = Column(String(255), nullable=False, unique=True, server_default=text("''"))
    share_email = Column(INTEGER(1), nullable=False, server_default=text("'8'"))
    email_bouncing = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    policy_class = Column(ForeignKey('tapir_policy_classes.class_id'), nullable=False, index=True, server_default=text("'0'"))
    joined_date = Column(INTEGER(10), nullable=False, index=True, server_default=text("'0'"))
    joined_ip_num = Column(String(16), index=True)
    joined_remote_host = Column(String(255), nullable=False, server_default=text("''"))
    flag_internal = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_edit_users = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_edit_system = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    flag_email_verified = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    flag_approved = Column(INTEGER(1), nullable=False, index=True, server_default=text("'1'"))
    flag_deleted = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_banned = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))
    flag_wants_email = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    flag_html_email = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    tracking_cookie = Column(String(255), nullable=False, index=True, server_default=text("''"))
    flag_allow_tex_produced = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    flag_can_lock = Column(INTEGER(1), nullable=False, index=True, server_default=text("'0'"))

    tapir_policy_classes = relationship('TapirPolicyClasses')
    username = relationship("TapirNicknames", uselist=False, viewonly=True)
    demographics = relationship("Demographics", uselist=False)
