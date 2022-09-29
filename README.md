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

There are two main things that are needed to use this with Flask.
1. All the models need to be imported and registered with the
   `arxiv_db.Base`
2. The metadata from `arxiv_db.Base` needs to be passed during the
   creation of the `SQLAlchemy` object.

    from flask import Flask, render_template
    from flask_sqlalchemy import SQLAlchemy
    import arxiv_db
    from arxiv_db.models import add_all_models_to_sqlalchemy

    # import all the model packages
    add_all_models_to_sqlalchemy()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://bob:passwd@localhost/arXiv"

    SQLAlchemy(app, metadata=arxiv_db.Base.metadata).init_app(app)

    from arxiv_db.models.tapir_users import TapirUsers

    @app.route("/users")
    def user_list():
        users = db.session.execute(db.select(TapirUsers).limit(10)).scalars()
        return render_template("list.html", users=users)

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
            
            
# I'd like better IDE completion
The result set returned from SQLalchemy isn't typed in a way that supports this.
Try:

    from sqlalchemy import create_engine, select
    from sqlalchemy.orm import Session
    import declartive_nooptions as models  # TODO rename this import
    
    engine = create_engine("mysql+pymysql://bob:passwd@localhost/arXiv")

    with Session(engine) as session:
        statement = select(models.OrcidIds).where(models.OrcidIds.orcid != None) .limit(10)
        result = session.execute(statement).scalars().all()
        for item in result:
            item: models.OrcidIds  # <----------- Add this to get IDE completion
            print(f"last:{item.last_name} email: {item.email} orcid:{item.orcid}") 
   
