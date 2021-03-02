from fastapi import FastAPI, HTTPException

from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware

from modapi.collab.collab_app import sio
import modapi.config as config
from . import schema

from modapi.services.arxiv_tables import arXiv_submissions


import databases
import sqlalchemy

SQLALCHEMY_DATABASE_URL = config.db_url
database = databases.Database(SQLALCHEMY_DATABASE_URL)
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)
metadata = sqlalchemy.MetaData()


fast_app = FastAPI()

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fast_app.on_event("startup")
async def startup():
    await database.connect()


@fast_app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@fast_app.get("/testRestToSocket")
async def rtos():
    """A test of emiting a socket.io event during a rest call"""
    await sio.emit("in_edit", {"id": "submission1234", "editor": "bob", "scope": "mod"})
    return {"did it": True}


#################### fast_api ####################


@fast_app.get("/status")
async def status():
    """Get the status of the ModAPI service."""
    return ""


@fast_app.post("/submission/modhold")
async def modhold(modhold: schema.ModHold):
    return modhold


@fast_app.get("/submission/{submission_id}", response_model=schema.Submission)
async def submission(submission_id: int):
    import pdb
    pdb.set_trace()
    query = arXiv_submissions.select().where(arXiv_submissions.c.submission_id == submission_id)
    return await database.fetch_one(query)


# @fast_app.get("/submission/{submission_id}")
# async def submission(submission_id: int):
#     return await submissions.get_submission(database, submission_id)

"""
Possible routes:

/queue/all
/queue/{cat}
/queue/{archive}

/queue/x/status/{int}
/queue/x/mods
/queue/x/proposals
/queue/x/submissions
/queue/x/?what else?

/submission/{subid}
/submission/{subid}/comments
/submission/{subid}/view_flag (still in use?)

/category_taxonomy

/next_publish
"""


########## LEGACY API SIGNATURES ##########
# @fast_app.get("/queue_alt/{submission_id}", response_model=List[schema.Submission])
# async def queue_alt(submission_id: Optional[int] = None):
#     return {"error": "not implemented"}


# @fast_app.get("/submission/{submission_id}")
# async def submission(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.get("/category_taxonomy")
# async def category_taxonomy():
#     return {"error": "not implemented"}


# @fast_app.get("/comments/{submission_id}")
# async def comments(submission_id: Optional[int] = None):
#     return {"error": "not implemented"}


# @fast_app.put("/comment/{submission_id}")
# async def comment(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.get("/proposals/{submission_id}")
# async def proposals(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.put("/proposals/{submission_id}")
# async def proposals(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.put("/proposal_response/{submission_id}")
# async def proposal_response(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.put("/category_rejection/{submission_id}")
# async def category_rejection(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.put("/category_promotion/{submission_id}")
# async def category_promotion(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.get("/moderators/{submission_id}")
# async def moderators(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.get("/classifier_scores/{submission_id}")
# async def classifier_scores(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.get("/categories/{submission_id}")
# async def categories(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.get("/view_flag/{submission_id}")
# async def view_flag(submission_id: int):
#     return {"error": "not implemented"}


# @fast_app.put("/view_flag/{submission_id}")
# async def view_flag_put(submission_id: int):
#     return {"error": "not implemented"}
