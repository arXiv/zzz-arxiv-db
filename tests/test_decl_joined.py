from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from arxiv_db.models import add_all_models_to_sqlalchemy
from arxiv_db.models.orcid_ids import *
from arxiv_db.models.tapir_users import TapirUsers

def test():
    engine = create_engine("mysql+pymysql://bdc34:onion@localhost/arXiv", echo=True)

    add_all_models_to_sqlalchemy()



    with Session(engine) as session:
        statement = select(OrcidIds).where(OrcidIds.orcid != None) .limit(10)
        result = session.execute(statement).scalars().all()
        for item in result:
            item: TapirUsers
            print(f"first:{item.first_name} last:{item.last_name} email: {item.email} orcid:{item.orcid}")
