from typing import List, Optional

from fastapi import APIRouter

from fastapi import HTTPException, Cookie, Depends
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse

from sqlalchemy.sql import select, and_

#from modapi.collab.collab_app import sio
import modapi.config as config

from modapi.db import database, engine

from modapi.auth import auth

from . import schema

from modapi.db.arxiv_tables import (
    arXiv_submissions,
    arXiv_submission_mod_hold,
    arXiv_admin_log,
    arXiv_submission_mod_flag,
    tapir_nicknames,
    submission_mod_flag_create
)

router = APIRouter()


@router.post("/submission/{submission_id}/modhold")
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


@router.post("/submission/{submission_id}/modhold/delete", response_model=str)
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


@router.get("/modholds", response_model=List[schema.ModHold])
async def modholds():
    """Gets all existing mod holds"""
    # TODO filter to just the holds for the user
    query = select(
        [arXiv_submission_mod_hold.c.submission_id, arXiv_submission_mod_hold.c.reason]
    ).select_from(arXiv_submission_mod_hold)

    return await database.fetch_all(query)



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
