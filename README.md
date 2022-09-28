# arXiv DB

SQLAlchemy models for arXiv DB tables.

# Install and test

    git clone git@github.com:arXiv/arxiv-db.git
    cd arxiv-db
    python3.8 -m venv ./venv  # or use pyenv
    source ./venv/bin/activate
    pip install poetry
    poetry install
    pytest

# Using Models

Here is an example of using SQLAlchemy ORM:

    from sqlalchemy import create_engine, select
    from sqlalchemy.orm import Session

    from arxiv_db.models import add_all_models_to_sqlalchemy
    add_all_models_to_sqlalchemy()

    from arxiv_db.models.tapir_users import TapirUsers

    engine = create_engine("mysql+pymysql://bdc34:onion@localhost/arXiv")

    with Session(engine) as session:
        statement = select(TapirUsers).limit(10)
        result = session.execute(statement).scalars().all()
        for item in result:
            print(f"{item.first_name} {item.last_name}")

