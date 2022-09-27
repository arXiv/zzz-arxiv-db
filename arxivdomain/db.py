from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine as _create_engine

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_engine(db_uri:str, echo:bool, args:dict):
    if 'sqlite' in db_uri:
        args["check_same_thread"]=False

    return _create_engine(db_uri, echo=echo, connect_args=args)


def create_tables(engine: Engine):
    """Create any missing tables."""
    import arxivdomain.tables.arxiv_tables as arxiv_tables
    arxiv_tables.metadata.create_all(bind=engine)
