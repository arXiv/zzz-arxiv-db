from sqlalchemy import Column, String

from .. import Base

metadata = Base.metadata


class AwsConfig(Base):
    __tablename__ = 'arXiv_aws_config'


    domain = Column(String(75), primary_key=True, nullable=False)
    keyname = Column(String(60), primary_key=True, nullable=False)
    value = Column(String(150))
