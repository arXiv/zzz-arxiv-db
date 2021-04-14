import testing.mysqld
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os
from multiprocessing import Process, Queue
import time


# Allows databases to work with testing.mysqld
# databases.Database.SUPPORTED_BACKENDS[
#     "mysql+pymysql"
# ] = databases.Database.SUPPORTED_BACKENDS["mysql"]


test_data = os.environ.get("TEST_SQL_DATA", "./tests/testdata.sql")


def escape_bind(stmt):
    return stmt.replace(':0', '\:0')


def launch_mysql(test_data, db_uri: Queue):
    print("Starting mysql...")
    with testing.mysqld.Mysqld() as mysqld:
        cmd_count = 0
        engine = create_engine(mysqld.url())
        metadata = sqlalchemy.MetaData()

        import modapi.db as db

        db.engine = engine
        db.metadata = metadata

        import modapi.db.arxiv_tables  # this import must be after db and metadata created

        metadata.create_all(engine)
        print("tables created")

        print("loading test data from file '{test_data}'...")
        with engine.connect() as conn:
            with open(test_data) as sql:
                cmd = ""

                for ln, line in enumerate(map(escape_bind, sql)):
                    if line.startswith("--"):
                        continue
                    elif line and line.rstrip().endswith(";"):
                        cmd = cmd + line
                        if cmd:
                            print(f"About to run '{cmd}'")
                            conn.execute(text(cmd))
                            cmd_count = cmd_count + 1
                            cmd = ""
                        else:
                            print("empty command")
                            cmd = ""
                    elif not line and cmd:
                        print(f"About to run '{cmd}'")
                        conn.execute(text(cmd))
                        cmd_count = cmd_count + 1
                        cmd = ""
                    elif not line:
                        continue
                    else:
                        cmd = cmd + line

        print(
            f""""
        Done loading test data: {cmd_count}
        
        DB URI is {mysqld.url()}
        
        If the mysql+pymysql causes a problem it can be replaced with just mysql.

        DB, ready. Waiting forever."""
        )
        db_uri.put(mysqld.url())
        while True:
            time.sleep(10)


def launch_modapi(classic_db_uri: str):
    os.environ["CLASSIC_DATABASE_URI"] = classic_db_uri.replace('+pymysql', '+aiomysql')
    from modapi.app import run_app
    run_app(False, # Cannot use reload with process.daemon
            False, # Cannot use uvicorn_debug with process.daemon
            True)  # Turn logging to DEBUG for modapi


if __name__ == "__main__":
    print("Starting the db process")
    db_uri_queue: Queue = Queue()
    db_process = Process(target=launch_mysql, args=(test_data, db_uri_queue))
    db_process.daemon = True
    db_process.start()

    print("Waiting for the db URI from the DB process")
    db_uri = db_uri_queue.get()  # blocking
    while not db_uri:
        time.sleep(1)
        db_uri = db_uri_queue.get()  # blocking

    print("Starting the API process")
    api_process = Process(target=launch_modapi, args=(db_uri,))
    api_process.daemon = True
    api_process.start()

    print(f"Test db_uri is {db_uri}")
    while True:
        time.sleep(10)

