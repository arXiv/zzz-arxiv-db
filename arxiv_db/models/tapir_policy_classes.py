from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, SMALLINT

from .. import Base

metadata = Base.metadata


class TapirPolicyClasses(Base):
    __tablename__ = 'tapir_policy_classes'


    class_id = Column(SMALLINT(5), primary_key=True)
    name = Column(String(64), nullable=False, server_default=text("''"))
    description = Column(Text, nullable=False)
    password_storage = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    recovery_policy = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    permanent_login = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
