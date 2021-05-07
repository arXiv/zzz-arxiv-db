from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

import modapi.config as config

import logging
log = logging.getLogger(__name__)


Base = declarative_base()
# """Global declarative base for use in SQLAlchemy ORM class
# definitions"""

engine = create_async_engine(config.db_url,
                             echo=config.echo_sql)                            
# """An async engine for use by the modapi"""


Session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    future=True
)
""" Session maker for use in API

# This is currently not a scoped session.

# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#using-a-sessionmaker"""


def create_tables():
    """Create any missing tables.

    This is a synchronous call"""
    from sqlalchemy import create_engine
    import modapi.tables.arxiv_tables
    sync_url = config.db_url.replace('+aiomysql', '')
    sync_eng = create_engine(sync_url,
                             echo=config.echo_sql)
    metadata.create_all(bind=sync_eng)
