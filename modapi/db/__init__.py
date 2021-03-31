
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
import modapi.config as config

engine = create_async_engine(config.db_url,
                             echo=config.debug)
"""An async engine for use by the modapi"""

Base = declarative_base()
"""Base for use in SQLAlchemy ORM class definitions"""


metadata = MetaData()
"""Avaiable to create Tables."""


def create_tables():
    """Create any missing tables.

    This is a synchronous call"""
    from sqlalchemy import create_engine
    import modapi.db.arxiv_tables
    sync_url = config.db_url.replace('+aiomysql', '')
    sync_eng = create_engine(sync_url,
                             echo=config.debug)
    metadata.create_all(bind=sync_eng)
