"""arXiv Moderator API"""

from fastapi import FastAPI, HTTPException
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.sql import text, select

from modapi.collab.collab_app import sio
import modapi.config as config

from modapi.db import database, engine, metadata

from . import schema

from modapi.services.arxiv_tables import arXiv_submissions, arXiv_submission_mod_hold

metadata.create_all(engine)

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
    await database.fetch_one(text("SELECT 1"))  # Test DB connection on startup


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
    """Get the status of the ModAPI service.

    Use the HTTP status code for the status. This returns an empty body on
    success.
    """
    await database.fetch_one(text("SELECT 1"))  # Test DB connection.
    return ""


@fast_app.post("/submission/modhold")
async def modhold(hold: schema.ModHold):
    """Put a submission on moderator hold."""

    # TODO use a transaction for all of this

    chk = (
        select([arXiv_submissions.c.status, arXiv_submission_mod_hold.c.reason])
        .select_from(arXiv_submissions.outerjoin(arXiv_submission_mod_hold))
        .where(arXiv_submissions.c.submission_id == hold.subid)
    )
    exists = await database.fetch_one(chk)

    if not exists:
        return JSONResponse(
            status_code=httpstatus.HTTP_409_CONFLICT,
            content={"msg": f" submission {hold.subid} not found"},
        )

    if exists and (exists["status"] == ON_HOLD or exists["reason"]):
        return JSONResponse(
            status_code=httpstatus.HTTP_409_CONFLICT,
            content={"msg": f"mod hold on {hold.subid} exists"},
        )

    # TODO need to decode the auth JWT to get the mod's username for the comment
    
    # TODO Set a admin_log comment so the admins will have some sort of idea about this.
    # addcomment = arXiv_admin_log.insert().values(
    #     username = ??,
    #     program = 'modapi.rest',
    #     command = 'modhold',
    #     logtext = f'moderator hold "{reason}"'
    #     submission_id = hold.subid,
    # )

    stmt = arXiv_submission_mod_hold.insert().values(
        submission_id=hold.subid, reason=hold.reason
    )
    await database.execute(stmt)
    return ""


@fast_app.get("/submission/{submission_id}", response_model=schema.Submission)
async def submission(submission_id: int):
    """Gets a submission. (WIP)"""
    query = arXiv_submissions.select().where(
        arXiv_submissions.c.submission_id == submission_id
    )
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

ON_HOLD = 2
"""Submission table status for on hold"""
