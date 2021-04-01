"""Routes for holds on submissions.

This works with the arXiv_submission_hold_reason table and is intended
to work for both mod and admin holds.

The paths in this module are intended to replace the /modhold paths.
"""
from enum import Enum
from typing import Optional, Union, List

from fastapi import APIRouter, Depends
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse
from modapi.auth import User, auth_user
from modapi.db import engine
from modapi.db.arxiv_tables import (
    arXiv_admin_log,
    arXiv_submissions,
    arXiv_submission_hold_reason,
)
from pydantic import BaseModel, conlist
from typing import Literal

from sqlalchemy import text

import logging
log = logging.getLogger(__name__)


router = APIRouter()


class ModHoldReasons(str, Enum):
    discussion = "discussion"
    moretime = "moretime"


class AdminHoldReasons(str, Enum):
    """All the admin reasons except 'other'"""

    scope = "scope"
    softreject = "softreject"
    hardreject = "hardreject"
    nonresearch = "nonresearch"
    salami = "salami"


class HoldType(str, Enum):
    admin = "admin"
    mod = "mod"


class HoldOut(BaseModel):
    type: HoldType
    username: Optional[str]
    reason: Optional[Union[ModHoldReasons, AdminHoldReasons]]


class AdminHoldIn(BaseModel):
    type: Literal["admin"]
    reason: AdminHoldReasons


class AdminOtherHoldIn(BaseModel):
    type: Literal["admin"]
    reason: Literal["other"]
    comment: str


class ModHoldIn(BaseModel):
    type: Literal["mod"]
    reason: ModHoldReasons


@router.post("/submission/{submission_id}/hold")
async def hold(
    submission_id: int,
    hold: Union[ModHoldIn, AdminHoldIn, AdminOtherHoldIn],
    user: User = Depends(auth_user),
):
    """Put a submission on hold."""
    if user.is_mod and not hold.type == "mod":
        return JSONResponse(status_code=403, content={"msg": "Unauthorized hold type"})

    async with engine.begin() as conn:
        exists = await _hold_check(submission_id)
        if not exists:
            return JSONResponse(
                status_code=httpstatus.HTTP_404_NOT_FOUND,
                content={"msg": f"submission {submission_id} not found"},
            )

        if exists and (exists["status"] == ON_HOLD or exists["reason"]):
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": f"Hold on {submission_id} already exists"},
            )

        if not (exists["status"] == 1 or exists["status"] == 4):
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={
                    "msg": "Can only put submissions in status 'submitted' or 'next'  to 'on hold'"
                },
            )

        stmt = arXiv_admin_log.insert().values(
            username=user.username,
            program="modapi.rest",
            command="hold",
            logtext=f'{hold.type} hold for "{hold.reason}"',
            submission_id=submission_id,
        )
        res = await conn.execute(stmt)
        comment_id = res.lastrowid

        stmt = arXiv_submission_hold_reason.insert().values(
            submission_id=submission_id,
            reason=hold.reason,
            user_id=user.user_id,
            type=hold.type,
            comment_id=comment_id,
        )
        await conn.execute(stmt)

        # TODO figure out if we need to set any datetimes on the submission row        
        stmt = (
            arXiv_submissions.update()
            .values(status=ON_HOLD)
            .where(arXiv_submissions.c.submission_id == submission_id)
        )
        await conn.execute(stmt)

        return "success"


@router.post("/submission/{submission_id}/hold/release", response_model=str)
async def hold_release(submission_id: int, user: User = Depends(auth_user)):
    """Releases a hold.

    If Moderator the submission must be:
    - on hold
    - have a row in arXiv_submission_hold_reason
    - have been created by this moderator

    If Admin the submission must be:
    - on hold
    """

    async with engine.begin() as conn:
        hold = await _hold_check(submission_id)
        if not hold:
            return JSONResponse(
                status_code=httpstatus.HTTP_404_NOT_FOUND,
                content={"msg": f" submission {submission_id} not found"},
            )

        [status, reason, hold_user_id, hold_type] = hold
        log.debug('hold_check was type: %s status: %s reason: %s',
                  hold_type, status, reason)

        if status != ON_HOLD:
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": f"{submission_id} is not on hold"},
            )

        if not user.is_admin and user.is_mod:
            if (hold_type != "mod" or reason is None):
                return JSONResponse(
                    status_code=httpstatus.HTTP_409_CONFLICT,
                    content={"msg": f"{submission_id} is not a mod hold"}
                )

        if reason:
            await conn.execute(
                arXiv_submission_hold_reason.delete().where(
                    arXiv_submission_hold_reason.c.submission_id == submission_id
                )
            )

        await conn.execute(
            arXiv_submissions.update()
            .values(status=SUBMITTED)
            .where(arXiv_submissions.c.submission_id == submission_id)
        )
        
        if hold_type is not None:
            logtext = f'release {hold_type} hold of reason "{reason}"'
        else:
            logtext = "release legacy hold"
            
        stmt = arXiv_admin_log.insert().values(
            username=user.username,
            program="modapi.rest",
            command="hold",
            logtext=logtext,
            submission_id=submission_id,
        )
        await conn.execute(stmt)
        
        # TODO Handle sticky_status? Is this is about the user taking
        # the sub to working and then resubmitting it?

        # TODO do correct release time. Super important for produciton
        # See arXiv::Schema::Result::Submission.propert_release_from_hold()
        return


@router.get(
    "/holds", response_model=List[conlist(Union[str, int], min_items=4, max_items=4)]
)
async def holds(user: User = Depends(auth_user)):
    """Gets all existing mod holds. 

    If the user is a moderator this only gets the holds on submissions
    of interest to the moderator.

    Returns List of [ subid, user_id, type, reason ]

    user_id, and reason may be an empty string.

    Type will be 'admin', 'mod' or 'legacy'.

    """
    async with engine.begin() as conn:
        if user.is_admin:
            query = """# All held submissions for admin
    SELECT s.submission_id, smh.reason, smh.user_id, smh.type
        FROM arXiv_submissions s
        LEFT JOIN arXiv_submission_hold_reason smh ON smh.submission_id = s.submission_id
        WHERE s.status IN (2)
    """
            rows = await conn.execute(text(query))
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
            rows = await conn.execute(text(query), {"userid": user.user_id})

    out = []
    for row in rows:
        (sub_id, reason, user_id, hold_type) = row
        out.append([int(sub_id),
                    user_id if user_id else '',                    
                    hold_type if hold_type else "legacy",
                    reason if reason else ''])

    return out


ON_HOLD = 2
"""Submission table status for on hold"""

SUBMITTED = 1
"""Submission table status for submitted and not on hold"""


async def _hold_check(submission_id: int):
    """Check for a hold.

    Returns None if no submission.

    Returns {status: int, user_id: int, reason: str} if submission exists and hold exists.

    Returns {status: int} if submission exists but hold doesn't exist
    in the hold table. This is might be a legacy style hold.

    """
    async with engine.begin() as conn:
        res = await conn.execute(text(
            # left join becasue we want to dstinguish between the
            # submission doesn't exist and submission is already on
            # mod-hold.
            """
            SELECT 
            s.status, shr.reason, shr.user_id, shr.type
            FROM
            arXiv_submissions s LEFT JOIN arXiv_submission_hold_reason shr
            ON s.submission_id = shr.submission_id
            WHERE s.submission_id = :submission_id
            """),
            {"submission_id": submission_id},
        )
        return list(res)[0]
