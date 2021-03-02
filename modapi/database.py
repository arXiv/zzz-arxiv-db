import databases
import sqlalchemy
import modapi.config as config

SQLALCHEMY_DATABASE_URL = config.db_url

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)
metadata = sqlalchemy.MetaData()

#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()
