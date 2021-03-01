import databases
import sqlalchemy

from modapi import config


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# database = None
# """Database for use by app"""

# engine = None
# """SQLAlchemy engine for use by app"""

# SessionLocal = None

# Base = None

# metadata is defined in arxiv_schema.py


# async def init_db(db_url: str):
#     """Init the DB for the app"""
#     global database
#     database = databases.Database(config.db_url)

#     global engine
#     engine = sqlalchemy.create_engine(
#         databases.Database(config.db_url),
#         connect_args={"check_same_thread": False}
#     )

#     global SessionLocal
#     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#     global Base
#     Base = declarative_base()
