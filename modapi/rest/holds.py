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
from modapi.db import Session
from modapi.tables.arxiv_tables import (
    arXiv_admin_log,
    arXiv_submissions,
    arXiv_submission_hold_reason,
)

from modapi.tables.arxiv_models import (
    Submissions,
    SubmissionCategory,
    SubmissionCategoryProposal,
)

from pydantic import BaseModel, conlist
from typing import Literal

from sqlalchemy import select, or_, and_, text
from sqlalchemy.orm import joinedload

import logging
log = logging.getLogger(__name__)


router = APIRouter()


class ModHoldReasons(str, Enum):
    discussion = "discussion"
    moretime = "moretime"


class SpecificRejectReasons(str, Enum):
    """All the admin reasons except 'other'"""

    scope = "scope"
    softreject = "softreject"
    hardreject = "hardreject"
    nonresearch = "nonresearch"
    salami = "salami"


RejectReasons = Union[SpecificRejectReasons, Literal["reject-other"]]


HoldReasons = Union[RejectReasons, Literal["other"]]


class HoldType(str, Enum):
    """mod holds can be released by mods,
    admin hold can be released only by admins"""
    admin = "admin"
    mod = "mod"


class HoldOut(BaseModel):
    type: HoldType
    username: Optional[str]
    reason: Optional[Union[ModHoldReasons, HoldReasons]]


class ModHoldIn(BaseModel):
    type: Literal["mod"]
    reason: ModHoldReasons


class RejectOther(BaseModel):
    """Reject the submission for some other reason with a comment"""
    type: Literal["admin"]
    reason: Literal["reject-other"]
    comment: str


class Reject(BaseModel):
    """Reject a submission with a reason from SpecificRejectReasons"""
    type: Literal["admin"]
    reason: SpecificRejectReasons


class SendToAdminOther(BaseModel):
    """"Put submission on hold with a comment"""
    type: Literal["admin"]
    reason: Literal["other"]
    comment: str
    sendback: bool


SendToAdminHolds = Union[Reject, RejectOther, SendToAdminOther]


@router.post("/submission/{submission_id}/hold")
async def hold(
        submission_id: int,
        hold: Union[ModHoldIn, SendToAdminHolds],
        user: User = Depends(auth_user),
):
    """Put a submission on hold

    This will prevent it from being announced until it is released from hold.

    The sendback feature is not yet implemented.
    """
    async with Session() as session:
        exists = await _hold_check(session, submission_id)
        if not exists:
            return JSONResponse(
                status_code=httpstatus.HTTP_404_NOT_FOUND,
                content={"msg": "submission not found"},
            )

        if exists and (exists["status"] == ON_HOLD or exists["reason"]):
            # It is critical that mods (or admins ) cannot put a mod
            # hold on a submission that is already on hold. This is to
            # avoid a mod from changing a legacy hold to a mod-hold or
            # admin-hold and then that mod releaseing the hold This
            # could be bad because it could allow a submission that is
            # on hold for serious non-moderatorion reasons to
            # accidently get published.  Reasons such as copyright or
            # failed TeX.
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": "Hold on submission already exists"},
            )

        if not (exists["status"] == 1 or exists["status"] == 4):
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={
                    "msg": "Can only put submissions in status 'submitted' or 'next'  to 'on hold'"
                },
            )

        oldstat = status_by_number.get(exists["status"], exists["status"])
        stmt = arXiv_admin_log.insert().values(
            username=user.username,
            program="modapi.rest",
            command="Hold",
            logtext=f"Status changed from '{oldstat}' to 'on hold', reason: {hold.reason}",
            submission_id=submission_id,
        )
        res = await session.execute(stmt)

        if hold.reason == "reject-other":
            logtext = f'Reject for other reason: {hold.comment}'
        elif hold.reason == "other":
            logtext = f'Hold and send to admins: {hold.comment}'
        else:
            logtext = f'{hold.type} hold for "{hold.reason}"'

        stmt = arXiv_admin_log.insert().values(
            username=user.username,
            program="Admin::Queue",
            command="admin comment",
            logtext=logtext,
            submission_id=submission_id,
        )
        res = await session.execute(stmt)
        comment_id = res.lastrowid

        stmt = arXiv_submission_hold_reason.insert().values(
            submission_id=submission_id,
            reason=hold.reason,
            user_id=user.user_id,
            type=hold.type,
            comment_id=comment_id,
        )
        await session.execute(stmt)

        # TODO figure out if we need to set any datetimes on the submission row
        stmt = (
            arXiv_submissions.update()
            .values(status=ON_HOLD)
            .where(arXiv_submissions.c.submission_id == submission_id)
        )
        await session.execute(stmt)
        await session.commit()
        return "success"


@router.post("/submission/{submission_id}/hold/release", response_model=str)
async def hold_release(submission_id: int, user: User = Depends(auth_user)):
    """Releases a hold.

    To release a hold means to set the submission status so that it is
    avaialbe to be published.

    If Moderator the submission must be:
    - on hold
    - have a row in arXiv_submission_hold_reason

    Moderators can release any hold that has a reason in the
    arXiv_submission_hold_reason table.

    If Admin the submission must be:
    - on hold

    Admins can release holds referenced in the
    arXiv_submission_hold_reason or legacy style holds.

    """
    # Seems like we shouldn't do the call to mod2 in the db transaction
    # TODO get the earliest_announce time for the submission

    async with Session() as session:
        hold = await _hold_check(session, submission_id)
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

        if not user.is_admin and user.is_moderator:
            if (hold_type != "mod" or reason is None):
                return JSONResponse(
                    status_code=httpstatus.HTTP_409_CONFLICT,
                    content={"msg": f"{submission_id} is not a mod hold"}
                )

        if reason:
            await session.execute(
                arXiv_submission_hold_reason.delete().where(
                    arXiv_submission_hold_reason.c.submission_id == submission_id
                )
            )

        await session.execute(
            arXiv_submissions.update()
            .values(status=SUBMITTED)
            .where(arXiv_submissions.c.submission_id == submission_id)
        )

        if hold_type is not None:
            logtext = f'Release: {hold_type} {reason} hold'
        else:
            logtext = "Release: legacy hold"

        stmt = arXiv_admin_log.insert().values(
            username=user.username,
            program="modapi.rest",
            command="hold_release",
            logtext=logtext,
            submission_id=submission_id,
        )
        await session.execute(stmt)

        stmt = arXiv_admin_log.insert().values(
            username=user.username,
            program="Admin::Queue",
            command="admin comment",
            logtext=logtext,
            submission_id=submission_id,
        )
        await session.execute(stmt)

        # TODO do correct release time. Super important for produciton
        # See arXiv::Schema::Result::Submission.propert_release_from_hold()

        await session.commit()


@router.get(
    "/holds", response_model=List[conlist(Union[str, int], min_items=4, max_items=4)]
)
async def holds(user: User = Depends(auth_user)):
    """Gets all existing holds.

    If the user is a moderator this only gets the holds on submissions
    of interest to the moderator.

    Returns List of [ subid, user_id, type, reason ]

    user_id, and reason may be an empty string.

    Type will be 'admin', 'mod' or 'legacy'.
    """
    async with Session() as session:
        query_options = [
            # Could deferre all of submission?
            joinedload(Submissions.hold_reasons),
        ]
        # TODO the admin query doesn't need any joins
        stmt = (select(Submissions)
                .outerjoin(Submissions.submission_category)
                .outerjoin(Submissions.proposals)
                .outerjoin(Submissions.hold_reasons)
                .options(*query_options)
                .filter(Submissions.status == ON_HOLD)
                )
        if user.is_moderator and not user.is_admin:
            cats = user.moderated_categories
            mod_ors = [
                SubmissionCategory.category.in_(cats),
                and_(SubmissionCategoryProposal.category.in_(cats),
                     SubmissionCategoryProposal.proposal_status == 0)
            ]
            for archive in user.moderated_archives:
                mod_ors.append(
                    SubmissionCategory.category.startswith(archive))
                # modui2 excluded subs with proposals in mod's archive
                # mod_ors.append(
                #     and_(SubmissionCategoryProposal.category.startswith(archive),
                #          SubmissionCategoryProposal.proposal_status == 0))

            stmt = stmt.filter(Submissions.type.in_(['new', 'rep', 'cross']))
            stmt = stmt.filter(or_(*mod_ors))

        res = await session.execute(stmt)
        out = []
        for row in res.unique():
            sub = row[0]
            if sub.hold_reasons:
                out.append([int(sub.submission_id),
                            sub.hold_reasons[0].user_id,
                            sub.hold_reasons[0].type,
                            sub.hold_reasons[0].reason])
            else:
                out.append([int(sub.submission_id),
                            '', 'legacy', ''])

        return out


ON_HOLD = 2
"""Submission table status for on hold"""

SUBMITTED = 1
"""Submission table status for submitted and not on hold"""


async def _hold_check(session, submission_id: int):
    """Check for a hold.

    Returns None if no submission.

    Returns {status: int, user_id: int, reason: str} if submission exists and hold exists.

    Returns {status: int} if submission exists but hold doesn't exist
    in the hold table. This is might be a legacy style hold.

    """
    res = await session.execute(text(
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


status_by_number = {
    # --- 'is_current' method statuses ( 0 - 4 )
    0: "working",  # incomplete; not submitted
    1: "submitted",
    2: "on hold",
    3: "unused",
    4: "next",  # for tomorrow
    # --- 'is_processing' method statuses (5 - 8)
    5: "processing",
    6: "needs_email",
    7: "published",
    8: "processing(submitting)",  # text extraction , etc
    #--- removed or error
    9: "removed",
    10: "user deleted",
    19: "error state",
    # --- expired (files removed) status are the above +20, usual ones are:
    20: 'deleted(working)',  # was working but expired
    22: 'deleted(on hold)',
    25: 'deleted(processing)',
    27: 'deleted(published)',  # published and files expired
    29: "deleted(removed)",
    30: 'deleted(user deleted)'  # user deleted and files expired
}
