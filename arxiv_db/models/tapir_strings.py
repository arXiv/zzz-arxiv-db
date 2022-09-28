from sqlalchemy import Column, String, Text, text

from .. import Base

metadata = Base.metadata


class TapirStrings(Base):
    __tablename__ = 'tapir_strings'


    name = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    module = Column(String(32), primary_key=True, nullable=False, server_default=text("''"))
    language = Column(String(32), primary_key=True, nullable=False, server_default=text("'en'"))
    string = Column(Text, nullable=False)
