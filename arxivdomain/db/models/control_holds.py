from typing import Optional, List
from sqlalchemy import BINARY, CHAR, Column, Date, DateTime, Enum, ForeignKey, ForeignKeyConstraint, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import types as types

from .. import Base

metadata = Base.metadata


class ControlHolds(Base):
    __tablename__ = 'arXiv_control_holds'

    __table_args__ = (
        Index('control_id', 'control_id', 'hold_type', unique=True),
    )

    hold_id = Column(INTEGER(10), primary_key=True)
    control_id = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    hold_type = Column(Enum('submission', 'cross', 'jref'), nullable=False, index=True, server_default=text("'submission'"))
    hold_status = Column(Enum('held', 'extended', 'accepted', 'rejected'), nullable=False, index=True, server_default=text("'held'"))
    hold_reason = Column(String(255), nullable=False, index=True, server_default=text("''"))
    hold_data = Column(String(255), nullable=False, server_default=text("''"))
    origin = Column(Enum('auto', 'user', 'admin', 'moderator'), nullable=False, index=True, server_default=text("'auto'"))
    placed_by = Column(ForeignKey('tapir_users.user_id'), index=True)
    last_changed_by = Column(ForeignKey('tapir_users.user_id'), index=True)

    tapir_users = relationship('TapirUsers', primaryjoin='ControlHolds.last_changed_by == TapirUsers.user_id')
    tapir_users1 = relationship('TapirUsers', primaryjoin='ControlHolds.placed_by == TapirUsers.user_id')
