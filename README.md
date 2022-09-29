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

# How to use with Flask?

TODO

# What about models that inherit?

Some models inherit from other models instead of Base. This is because
the represent tables that lack primary key. Use them as you would any
other table:

    from sqlalchemy import create_engine, select
    from sqlalchemy.orm import Session
    import declartive_nooptions as models  # TODO rename this import
    
    engine = create_engine("mysql+pymysql://bob:passwd@localhost/arXiv")

    with Session(engine) as session:
        statement = select(models.ArXivOrcidIds).where(models.ArXivOrcidIds.orcid != None) .limit(10)
        result = session.execute(statement).scalars().all()
        for item in result:
            print(f"last:{item.last_name} email: {item.email} orcid:{item.orcid}")
    
