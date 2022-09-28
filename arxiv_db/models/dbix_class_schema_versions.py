from sqlalchemy import Column, String

from .. import Base

metadata = Base.metadata


class DbixClassSchemaVersions(Base):
    __tablename__ = 'dbix_class_schema_versions'


    version = Column(String(10), primary_key=True)
    installed = Column(String(20), nullable=False)
