
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
import modapi.config as config

SQLALCHEMY_DATABASE_URL = config.db_url

#database = databases.Database(SQLALCHEMY_DATABASE_URL)
"""Databases for async execution of SQL statements.

Note about Databases and SQLAlchemy setup:

We'd like to do async calls to the DB for performance.  Sqlalchemy
does not directly support async so the patern of use here is to
create the SQL with sqlalchemy and then execute it with the Databases
async library.

Using SQLAlchemy Core is documented at fast-api and Databases. Using
SqlAlchemy ORM is not documented.

For a description of SQLAlchemy see 
https://docs.sqlalchemy.org/en/13/core/tutorial.html

For using queryies with Databases see
https://github.com/encode/databases/blob/master/docs/database_queries.md

"""

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()

metadata = MetaData()
"""Avaiable to create Tables."""
