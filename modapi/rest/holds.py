"""Routes for holds on submissions"""
from enum import Enum
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse
from modapi.auth import Auth, User, auth, auth_user
from modapi.db import database
from modapi.db.arxiv_tables import (arXiv_admin_log, arXiv_submission_mod_flag,
                                    arXiv_submission_mod_hold,
                                    arXiv_submissions,
                                    submission_mod_flag_create,
                                    tapir_nicknames)
from pydantic import BaseModel
from sqlalchemy.sql import and_, select

from . import schema

router = APIRouter()


class HoldReasons(str, Enum):
    discussion = "discussion"
    moretime = "moretime"


class HoldType(str, Enum):
    admin = "admin"
    mod = "mod"


class HoldOut(BaseModel):
    type: HoldType
    username: Optional[str]
    reason: Optional[HoldReasons]


class HoldIn(BaseModel):
    """Hold for input to hold()"""

    type: HoldType
    reason: HoldReasons


@router.post("/submission/{submission_id}/hold")
async def hold(submission_id: int, hold: HoldIn, user: User = Depends(auth_user)):
    """Put a submission on moderator hold."""
    async with database.transaction():
        exists = await _hold_check(hold.submission_id)
        if not exists:
            return JSONResponse(
                status_code=httpstatus.HTTP_404_NOT_FOUND,
                content={"msg": f"submission {hold.submission_id} not found"},
            )

        if exists and (exists["status"] == ON_HOLD or exists["reason"]):
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": f"Hold on {hold.submission_id} already exists"},
            )

        stmt = arXiv_admin_log.insert().values(
            username=user.username,
            program="modapi.rest",
            command="modhold",
            logtext=f'moderator hold for "{hold.reason}"',
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

        return f"success"


@router.post("/submission/{submission_id}/hold/release", response_model=str)
async def hold_release(submission_id: int):
    """Releases a hold.

    If Moderator the submission must be:
    - on hold
    - have a row in arXiv_submission_mod_hold
    - have been created by this moderator

If Admin the submission must be:
    - on hold
    """
    async with database.transaction():
        hold = await _hold_check(submission_id)
        if not hold:
            return JSONResponse(
                status_code=httpstatus.HTTP_404_NOT_FOUND,
                content={"msg": f" submission {submission_id} not found"},
            )

        [status, reason, hold_user_id] = hold

        if status != ON_HOLD:
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": f"{submission_id} is not on hold"},
            )

        if not user.is_admin:
            if "reason" not in hold or hold["reason"] is None:
                return JSONResponse(
                    status_code=httpstatus.HTTP_409_CONFLICT,
                    content={"msg": f"{submission_id} is on ADMIN hold"},
                )
            if user.user_id != hold_user_id:
                return JSONResponse(
                    status_code=httpstatus.HTTP_409_CONFLICT,
                    content={"msg": f"{submission_id} is not held by this mod."},
                )

        if reason:
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
        # TODO Handle sticky_status? Maybe not important? Is this is about
        # the user taking the sub to working and then resubmitting it.

        # TODO do correct release time. Super important for produciton
        # See arXiv::Schema::Result::Submission.propert_release_from_hold()
        return f"{mh_n} {s_n}"


@router.get("/holds", response_model=Dict[int, HoldOut])
async def holds(user: User = Depends(auth_user)):
    """Gets all existing mod holds"""

    """
    input: user_id

    
    """
    if user.is_admin:
        import pdb; pdb.set_trace()
        query = """# All held submissions for admin
SELECT s.submission_id, smh.reason, smh.user_id, smh.type
    FROM arXiv_submissions s
    LEFT JOIN arXiv_submission_hold_reason smh ON smh.submission_id = s.submission_id
    WHERE s.status IN (2)
"""
        rows = await database.fetch_all(query)
    else:
        query = """
# submissions on hold in mod's categories
SELECT s.submission_id, smh.reason, smh.user_id, smh.type
    FROM arXiv_submissions s
    JOIN arXiv_submission_category sc ON s.submission_id=sc.submission_id
    JOIN arXiv_moderators m ON sc.category=concat_ws(".", m.archive, NULLIF(m.subject_class, ""))
    LEFT JOIN arXiv_submission_hold_reason smh ON smh.submission_id = s.submission_id
    WHERE s.status IN (2) AND m.user_id=:userid
UNION
# unresolved proposal holds for mod's categories
SELECT  s.submission_id, smh.reason, smh.user_id, smh.type
    FROM arXiv_submissions s
    JOIN arXiv_submission_category_proposal scp ON s.submission_id=scp.submission_id
    JOIN arXiv_moderators m ON scp.category=concat_ws(".", m.archive, NULLIF(m.subject_class, ""))
    LEFT JOIN arXiv_submission_hold_reason smh ON smh.submission_id = s.submission_id
    WHERE s.status IN (2) AND m.user_id=:userid AND scp.proposal_status = 0
"""
        rows = await database.fetch_all(query, {"userid": user.user_id})

    holds = {}
    for row in rows:
        (id, reason, user_id, type) = row
        if id in holds:
            continue  # strange, we shoudn't have a multiple holds for a submisison

        legacy_hold = not type
        holds[int(id)] = {
            "reason": reason,
            "user_id": user_id,
            "type": type if not legacy_hold else "admin",
        }

    return holds


ON_HOLD = 2
"""Submission table status for on hold"""

SUBMITTED = 1
"""Submission table status for submitted and not on hold"""


async def _hold_check(submission_id: int):
    """Check for a hold.

    Returns None if no submission.

    Returns {status: int, reason: str} if submission exists and hold exists.

    Returns {status: int} if submission exists but hold doesn't exist
    in the hold table. This is might be a legacy style hold.

    """
    return await database.fetch_one(
        # outer join becasue we want to dstinguish between submission
        # doesn't exist and submission is already on mod-hold.
        select(
            [
                arXiv_submissions.c.status,
                arXiv_submission_mod_hold.c.reason,
                arXiv_submission_mod_hold.user_id,
            ]
        )
        .select_from(arXiv_submissions.outerjoin(arXiv_submission_mod_hold))
        .where(arXiv_submissions.c.submission_id == submission_id)
    )
