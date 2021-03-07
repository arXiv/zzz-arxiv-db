"""arXiv Moderator API"""
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Cookie, Depends
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.sql import text, select, and_

from modapi.collab.collab_app import sio
import modapi.config as config

from modapi.db import database, engine, metadata

from modapi.auth import decode

from . import schema

from modapi.db.arxiv_tables import (
    arXiv_submissions,
    arXiv_submission_mod_hold,
    arXiv_admin_log,
    arXiv_submission_mod_flag,
    tapir_nicknames
)

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
#    await database.fetch_one(text("SELECT 1"))  # Test DB connection on startup


@fast_app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

    
async def ng_jwt(ARXIVNG_SESSION_ID: Optional[str] = Cookie(None)):
    return decode(ARXIVNG_SESSION_ID, config.jwt_secret)


# @fast_app.get("/testRestToSocket")
# async def rtos():
#     """A test of emiting a socket.io event during a rest call"""
#     await sio.emit("in_edit", {"id": "submission1234", "editor": "bob", "scope": "mod"})
#     return {"did it": True}


#################### fast_api ####################


@fast_app.get("/status")
async def status(jwt: Optional[dict] = Depends(ng_jwt)):
    """Get the status of the ModAPI service.

    Use the HTTP status code for the status. This returns an empty body on
    success.
    """
    #await database.fetch_one(text("SELECT 1"))  # Test DB connection.
    ###    data = decode(ARXIVNG_SESSION_ID, config.jwt_secret)
    # return data
    #return jwt
    return ''


# @fast_app.get("/submission/{submission_id}", response_model=schema.Submission)
# async def submission(submission_id: int):
#     """Gets a submission. (WIP)"""
#     query = arXiv_submissions.select().where(
#         arXiv_submissions.c.submission_id == submission_id
#     )
#     return await database.fetch_one(query)


@fast_app.post("/submission/{submission_id}/modhold")
async def modhold(submission_id: int, hold: schema.ModHold):
    """Put a submission on moderator hold."""
    
    # TODO use a transaction for all of this
    exists = await _modhold_check(hold.submission_id)
    if not exists:
        return JSONResponse(
            status_code=httpstatus.HTTP_404_NOT_FOUND,
            content={"msg": f" submission {hold.submission_id} not found"},
        )

    if exists and (exists["status"] == ON_HOLD or exists["reason"]):
        return JSONResponse(
            status_code=httpstatus.HTTP_409_CONFLICT,
            content={"msg": f"mod hold on {hold.submission_id} exists"},
        )

    # TODO don't let mods put submissions in strange statuses on hold
    
    # TODO need to decode the auth JWT to get the mod's username for the comment

    # TODO Set a admin_log comment so the admins will have some sort of idea about this.
    stmt = arXiv_admin_log.insert().values(
        username="TODO",
        program="modapi.rest",
        command="modhold",
        logtext=f'moderator hold "{hold.reason}"',
        submission_id=hold.submission_id,
    )
    comment_id = await database.execute(stmt)

    stmt = arXiv_submission_mod_hold.insert().values(
        submission_id=hold.submission_id, reason=hold.reason, comment_id=comment_id
    )
    await database.execute(stmt)

    stmt = (
        arXiv_submissions.update()
        .values(status=ON_HOLD)
        .where(arXiv_submissions.c.submission_id == hold.submission_id)
    )
    await database.execute(stmt)

    return f"success, logcomment {comment_id}"


@fast_app.post("/submission/{submission_id}/modhold/delete", response_model=str)
async def modhold_delete(submission_id: int):
    """Releases a mod hold. 

    The submission must be both on hold and have a row in
    arXiv_submission_mod_hold.
    """
    exists = await _modhold_check(submission_id)
    if not exists:
        return JSONResponse(
            status_code=httpstatus.HTTP_404_NOT_FOUND,
            content={"msg": f" submission {submission_id} not found"},
        )
    elif exists["status"] != ON_HOLD:
        return JSONResponse(
            status_code=httpstatus.HTTP_409_CONFLICT,
            content={"msg": f"{submission_id} is not on hold"},
        )
    elif "reason" not in exists or exists["reason"] is None:
        return JSONResponse(
            status_code=httpstatus.HTTP_409_CONFLICT,
            content={"msg": f"{submission_id} is on ADMIN hold"},
        )

    mh_n = await database.execute(
        arXiv_submission_mod_hold.delete().where(
            arXiv_submission_mod_hold.c.submission_id == submission_id
        )
    )

    s_n = await database.execute(
        arXiv_submissions.update()
        .values(status=SUBMITTED)
        .where(arXiv_submissions.c.submission_id == submission_id)
    )
    #TODO sticky_status?
    #TODO do correct release time. See arXiv::Schema::Result::Submission.propert_release_from_hold()
    return f"{mh_n} {s_n}"


@fast_app.get("/modholds", response_model=List[schema.ModHold])
async def modholds():
    """Gets all existing mod holds"""
    # TODO filter to just the holds for the user
    query = select(
        [arXiv_submission_mod_hold.c.submission_id, arXiv_submission_mod_hold.c.reason]
    ).select_from(arXiv_submission_mod_hold)

    return await database.fetch_all(query)



@fast_app.put("/submission/{submission_id}/flag")
async def put_flag(submission_id: int, flag: schema.ModFlag):
    # TODO validate user

    # TODO handle duplicate entry better, right now it is a 500
    # due to a pymysql.err.IntegrityError. Do a 409
    stmt = arXiv_submission_mod_flag.insert().values(
        user_id=flag.user_id,
        flag=schema.modflag_to_int[flag.flag],
        submission_id=submission_id,
    )
    await database.execute(stmt)


@fast_app.post("/submission/{submission_id}/flag/delete")
async def del_flag(submission_id: int, flag: schema.ModFlagDel):
    # validate user

    # TODO check that user owns the flag

    await database.execute(
        arXiv_submission_mod_flag.delete()
        .where( and_(arXiv_submission_mod_flag.c.submission_id == submission_id,
                     arXiv_submission_mod_flag.c.user_id == flag.user_id ))
    )
    

@fast_app.get("/flags", response_model=List[schema.ModFlagOut])
async def modflags():
    """Gets list of submissions with checkmarks"""
    # TODO check the user
    
    # TODO filter to just the checkmarks for the user
    query = select(
        [arXiv_submission_mod_flag.c.submission_id,
         arXiv_submission_mod_flag.c.updated,
         text('tapir_nicknames.nickname as username')]
    ).select_from(arXiv_submission_mod_flag
                  .join(tapir_nicknames,
                        arXiv_submission_mod_flag.c.user_id == tapir_nicknames.c.user_id))

    return await database.fetch_all(query)




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

SUBMITTED = 1
"""Submission table status for submitted and not on hold"""

async def _modhold_check(submission_id: int):
    """Check for a mod hold.

    Returns None if no submission.

    Returns {status: int, reason: str} if submission exists and mod hold exists.

    Returns {status: int} if submission exists but mod hold doesn't exist.
    """
    chk = (
        # outer join becasue we want to dstinguish between submission
        # doesn't exist and submission is already on mod-hold.
        select([arXiv_submissions.c.status, arXiv_submission_mod_hold.c.reason])
        .select_from(arXiv_submissions.outerjoin(arXiv_submission_mod_hold))
        .where(arXiv_submissions.c.submission_id == submission_id)
    )
    return await database.fetch_one(chk)
