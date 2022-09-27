from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine as _create_engine

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(metaclass=DeclarativeMeta):
    """Non-dynamic base for better types.

    see https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#creating-an-explicit-base-non-dynamically-for-use-with-mypy-similar
    """
    __abstract__ = True
    registry = mapper_registry
    metadata = mapper_registry.metadata
    __init__ = mapper_registry.constructor

def create_engine(db_uri:str, echo:bool, args:dict):
    if 'sqlite' in db_uri:
        args["check_same_thread"]=False

    return _create_engine(db_uri, echo=echo, connect_args=args)


def create_tables(engine: Engine):
    """Create any missing tables."""
    import arxivdomain.tables.arxiv_tables as arxiv_tables
    arxiv_tables.metadata.create_all(bind=engine)
