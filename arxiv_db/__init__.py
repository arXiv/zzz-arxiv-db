from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine as _create_engine
from sqlalchemy.orm import registry
from sqlalchemy.orm.decl_api import DeclarativeMeta

mapper_registry = registry()

class Base(metaclass=DeclarativeMeta):
    """Non-dynamic base for better types.

    See
    https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#creating-an-explicit-base-non-dynamically-for-use-with-mypy-similar
    """
    __abstract__ = True
    registry = mapper_registry
    metadata = mapper_registry.metadata
    __init__ = mapper_registry.constructor

def create_engine(db_uri:str, echo:bool, args:dict):
    if 'sqlite' in db_uri:
        args["check_same_thread"]=False

    return _create_engine(db_uri, echo=echo, connect_args=args)

def init_with_flask_sqlalchemy(db):
    """Takes a flask_sqlalchemy.SQLAlchemy object and uses that as Base.

    This allows the models and tables in this package to be used with
    flask_sqlalchemy.
    """
    global Base
    Base = db


def create_tables(engine: Engine):
    """Create any missing tables."""
    from .tables import arxiv_tables
    arxiv_tables.metadata.create_all(bind=engine)
