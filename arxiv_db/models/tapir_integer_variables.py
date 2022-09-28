from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import INTEGER

from .. import Base

metadata = Base.metadata


class TapirIntegerVariables(Base):
    __tablename__ = 'tapir_integer_variables'


    variable_id = Column(String(32), primary_key=True, server_default=text("''"))
    value = Column(INTEGER(4), nullable=False, server_default=text("'0'"))
