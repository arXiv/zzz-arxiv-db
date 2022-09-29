from sqlalchemy import BINARY, BigInteger, CHAR, Column, Date, DateTime, Enum, ForeignKeyConstraint, Index, Integer, JSON, SmallInteger, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import CHAR, DECIMAL, INTEGER, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship

from .. import Base

metadata = Base.metadata

# tapir_demographics

from .tapir_users import TapirUsers

class TapirDemographics(TapirUsers):
    __tablename__ = 'tapir_demographics'
    __table_args__ = (
        ForeignKeyConstraint(['country'], ['tapir_countries.digraph'], name='0_518'),
        ForeignKeyConstraint(['user_id'], ['tapir_users.user_id'], name='0_517'),
        Index('birthday', 'birthday'),
        Index('country', 'country'),
        Index('postal_code', 'postal_code')
    )

    user_id = Column(INTEGER, primary_key=True, server_default=text("'0'"))
    gender = Column(Integer, nullable=False, server_default=text("'0'"))
    share_gender = Column(INTEGER, nullable=False, server_default=text("'16'"))
    share_birthday = Column(INTEGER, nullable=False, server_default=text("'16'"))
    country = Column(CHAR(2), nullable=False, server_default=text("''"))
    share_country = Column(INTEGER, nullable=False, server_default=text("'16'"))
    postal_code = Column(String(16), nullable=False, server_default=text("''"))
    birthday = Column(Date)

    tapir_countries = relationship('TapirCountries', back_populates='tapir_demographics')
