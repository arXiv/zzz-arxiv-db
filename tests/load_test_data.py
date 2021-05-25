import os

from sqlalchemy import create_engine
from sqlalchemy.sql import text

test_data = os.environ.get("TEST_SQL_DATA", "./tests/testdata.sql")


def escape_bind(stmt):
    return stmt.replace(':0', '\:0')


def load_example_data(engine):
    print("loading test data from file '{test_data}'...")
    cmd_count = 0
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

    print(f"Done loading test data: {cmd_count}")


if __name__ == "__main__":
    uri = os.environ["CLASSIC_DATABASE_URI"]
    engine = create_engine(uri)
    import modapi.db.arxiv_tables as tables
    tables.metadata.create_all(bind=engine)
    load_example_data(engine)
