from sqlalchemy import Column, String, Text, text

from .. import Base

metadata = Base.metadata


class TapirStringVariables(Base):
    __tablename__ = 'tapir_string_variables'


    variable_id = Column(String(32), primary_key=True, server_default=text("''"))
    value = Column(Text, nullable=False)

