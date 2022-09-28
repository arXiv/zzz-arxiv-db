from sqlalchemy import CHAR, Column, String, text
from sqlalchemy.dialects.mysql import CHAR, INTEGER

from .. import Base

metadata = Base.metadata


class TapirCountries(Base):
    __tablename__ = 'tapir_countries'


    digraph = Column(CHAR(2), primary_key=True, server_default=text("''"))
    country_name = Column(String(255), nullable=False, server_default=text("''"))
    rank = Column(INTEGER(1), nullable=False, server_default=text("'255'"))
