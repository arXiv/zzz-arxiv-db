"""Routes for holds on submissions.

This works with the arXiv_submission_hold_reason table and is intended
to work for both mod and admin holds.

The paths in this module are intended to replace the /modhold paths.
"""
from enum import Enum
from typing import Optional, Union, List
from datetime import datetime
import pytz
from dataclasses import dataclass, field
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse
from modapi.auth import User, auth_user
from modapi.db import get_db
from modapi.rest.earliest_announce import earliest_announce

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

from sqlalchemy import select, or_, and_, text, null
from sqlalchemy.orm import joinedload

import logging
log = logging.getLogger(__name__)


router = APIRouter()


class ModHoldReasons(str, Enum):
    """Reasons for mod holds"""
    discussion = "discussion"
    moretime = "moretime"


class HoldType(str, Enum):
    """mod holds can be released by mods,
    admin hold can be released only by admins"""
    admin = "admin"
    mod = "mod"


class ModHoldIn(BaseModel):
    type: Literal["mod"]
    reason: ModHoldReasons


class RejectOther(BaseModel):
    """Reject the submission for some other reason with a comment"""
    type: Literal["admin"]
    reason: Literal["reject-other"]
    comment: str


class SpecificRejectReasons(str, Enum):
    """All the admin reasons except 'other'"""
    scope = "scope"
    softreject = "softreject"
    hardreject = "hardreject"
    nonresearch = "nonresearch"
    salami = "salami"


RejectReasons = Union[SpecificRejectReasons, Literal["reject-other"]]

HoldReasons = Union[RejectReasons, Literal["other"]]


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

HoldTypes = Union[ModHoldIn, SendToAdminHolds]


class HoldOut(BaseModel):
    """Holds for use in results of requests"""
    type: HoldType
    username: Optional[str]
    reason: Optional[Union[ModHoldReasons, HoldReasons]]


@dataclass
class HoldLogicRes():
    visible_comments: List[str] =  field(default_factory=list)
    modapi_comments: List[str] =  field(default_factory=list)
    delete_hold_reason: bool = False
    create_hold_reason: bool = False


def _hold_comments(hold: HoldTypes) -> List[str]:
    """Returns a list of comments that should be stored in the admin log in order
    in a way that will be visible to admins and mods."""
    if hold.type == 'mod':
        return [f'Mod Hold reason: {hold.reason}']
    elif hold.type == 'admin':
        if hold.reason == 'other':
            return ['Admin Hold for reason: other. '
                    f'sendback: {str(hold.sendback)} comment: {hold.comment}']
        elif hold.reason == 'reject-other':
            return ['Admin Hold and Reject for reason: reject-other'
                    f' with comment: {hold.comment}']
        else:
            return [f'Admin Hold and Reject for reason: {hold.reason}']
    else:
        return [f'Hold of type {hold.type}']


def _hold_biz_logic(hold: HoldTypes, exists, submission_id: int, user: User) -> Union[HoldLogicRes, JSONResponse]:
    if not exists:
        return JSONResponse(status_code=httpstatus.HTTP_404_NOT_FOUND,
                            content={"msg": "submission not found"})

    if exists["is_locked"]:  # This is hard locked, not an edit collab lock
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN,
                            content={"msg": f"{submission_id} is locked"})

    if not (exists["status"] in [1, 4, 2]):  # hold is included since some held subs can be held again
        return JSONResponse(status_code=httpstatus.HTTP_409_CONFLICT,
                            content={"msg": "Can only hold submissions in that status"})

    oldstat = status_by_number.get(exists["status"], exists["status"])
    rv = HoldLogicRes(
        modapi_comments=[f"Status changed from '{oldstat}' to 'on hold', reason: {hold.reason}"],
        visible_comments=_hold_comments(hold))

    if hold.type == 'mod':
        if exists["status"] == ON_HOLD or exists["reason"]:
            # Mods cannot put a mod hold on a submission that is
            # already on admin or legacy hold. This is to avoid a
            # mod from changing a legacy hold to a mod-hold and
            # then that mod releaseing the hold. This would allow
            # a submission that is on hold for non-moderatorion
            # reasons such as copyright or failed TeX to
            # accidently get published.
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": "Hold on submission already exists"})
        else:
            rv.create_hold_reason = True

    elif hold.type == 'admin':
        if exists["status"] != ON_HOLD and not exists["reason"]:  # not on hold
            rv.create_hold_reason = True
        elif exists["status"] == ON_HOLD and exists["reason"]:  # on mod hold
            rv.delete_hold_reason = True
            rv.create_hold_reason = True
            rv.visible_comments.insert(0, "Clear modhold, about to admin hold")
            rv.modapi_comments.insert(0, "Clear modhold")
        else:
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": "Admin hold on submission already exists"})
    else:
        return JSONResponse(status_code=httpstatus.HTTP_400_BAD_REQUEST,
                            content={"msg": "invalid hold type"})

    return rv


@router.post("/submission/{submission_id}/hold")
async def hold(
        submission_id: int,
        hold: HoldTypes,
        user: User = Depends(auth_user),
        db: Session = Depends(get_db)
):
    """Put a submission on hold

    This will prevent it from being announced until it is released from hold.

    The sendback feature is not yet implemented.
    """
    exists = _hold_check(db, submission_id)

    hold_res = _hold_biz_logic(hold, exists, submission_id, user)
    if not isinstance(hold_res, HoldLogicRes):
        return hold_res

    for logtext in hold_res.modapi_comments:
        stmt = arXiv_admin_log.insert().values(
            submission_id=submission_id, username=user.username,
            program="modapi.rest", command="Hold", logtext=logtext)
        res = db.execute(stmt)

    for logtext in hold_res.visible_comments:
        stmt = arXiv_admin_log.insert().values(
            submission_id=submission_id, username=user.username,
            program="Admin::Queue", command="admin comment",
            logtext=logtext
        )
        res = db.execute(stmt)
        comment_id = res.lastrowid

    if hold_res.delete_hold_reason:
        db.execute(arXiv_submission_hold_reason.delete()
                   .where(arXiv_submission_hold_reason.c.submission_id == submission_id))

    if hold_res.create_hold_reason:
        stmt = arXiv_submission_hold_reason.insert().values(
            submission_id=submission_id, comment_id=comment_id, user_id=user.user_id,
            type=hold.type, reason=hold.reason)
        db.execute(stmt)

    stmt = (arXiv_submissions.update()
            .values(status=ON_HOLD)
            .where(arXiv_submissions.c.submission_id == submission_id))
    db.execute(stmt)
    db.commit()
    return "success"


@router.post("/submission/{submission_id}/hold/release", response_model=str)
async def hold_release(submission_id: int, user: User = Depends(auth_user),
                       db: Session = Depends(get_db)):
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
    hold = _hold_check(db, submission_id)
    if not hold:
        return JSONResponse(
            status_code=httpstatus.HTTP_404_NOT_FOUND,
            content={"msg": "submission not found"})

    [status, reason, hold_user_id, hold_type, submit_time, sticky_status, is_locked] = hold

    if is_locked:
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN,
                            content={"msg": f"{submission_id} is locked"})

    if not user.is_admin and user.is_moderator:
        if (hold_type != "mod" or reason is None):
            return JSONResponse(
                status_code=httpstatus.HTTP_403_FORBIDDEN,
                content={"msg": f"{submission_id} is not a mod hold"})

    anno_time = await earliest_announce(submission_id)
    if reason:
        db.execute(arXiv_submission_hold_reason.delete()
                   .where(arXiv_submission_hold_reason.c.submission_id == submission_id))

    # Do correct release time and stick_status
    # See arXiv::Schema::Result::Submission.propert_release_from_hold()
    db.execute(arXiv_submissions.update()
               .values(sticky_status=null())
               .where(arXiv_submissions.c.submission_id == submission_id))

    if submit_time:
        db.execute(arXiv_submissions.update()
                   .values(status=SUBMITTED)
                   .where(arXiv_submissions.c.submission_id == submission_id))
        now = datetime.now(tz=pytz.timezone('US/Eastern'))
        if now > anno_time:
            db.execute(arXiv_submissions.update()
                       .values(release_time=now)
                       .where(arXiv_submissions.c.submission_id == submission_id))
    else:
        db.execute(arXiv_submissions.update()
                   .values(status=WORKING)
                   .where(arXiv_submissions.c.submission_id == submission_id))

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
    db.execute(stmt)

    stmt = arXiv_admin_log.insert().values(
        username=user.username,
        program="Admin::Queue",
        command="admin comment",
        logtext=logtext,
        submission_id=submission_id,
    )
    db.execute(stmt)
    db.commit()
    return "success"


@router.get("/holds", response_model=List[conlist(Union[str, int], min_items=4, max_items=4)])
async def holds(user: User = Depends(auth_user), db: Session = Depends(get_db)):
    """Gets all existing holds.

    If the user is a moderator this only gets the holds on submissions
    of interest to the moderator.

    Returns List of [ subid, user_id, type, reason ]

    user_id, and reason may be an empty string.

    Type will be 'admin', 'mod' or 'legacy'.
    """
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

    res = db.execute(stmt)
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

WORKING = 0
"""Submission table status for not yet submitted"""


def _hold_check(db: Session, submission_id: int):
    """Check for a hold.

    Returns None if no submission.

    Returns {status: int, user_id: int, reason: str} if submission exists and hold exists.

    Returns {status: int} if submission exists but hold doesn't exist
    in the hold table. This is might be a legacy style hold.

    """

    res = db.execute(text(
        # left join becasue we want to dstinguish between the
        # submission doesn't exist and submission is already on
        # mod-hold.
        """
        SELECT
        s.status, shr.reason, shr.user_id, shr.type, s.submit_time, s.sticky_status, s.is_locked
        FROM
        arXiv_submissions s LEFT JOIN arXiv_submission_hold_reason shr
        ON s.submission_id = shr.submission_id
        WHERE s.submission_id = :submission_id
        """),
        {"submission_id": submission_id},
    )
    sub = res.first()
    if sub:
        [status, reason, hold_user_id, hold_type, submit_time, sticky_status, is_locked] = sub
        log.debug('For sub %d hold_check was type: %s status: %s reason: %s sticky_status: %s is_locked: %s submit_time %s',
                  submission_id, hold_type, status, reason, sticky_status, is_locked, submit_time)
        return sub
    else:
        return None


status_by_number = {
    0: "working",  # incomplete; not submitted
    1: "submitted",
    2: "on hold",
    3: "unused",
    4: "next",  # for tomorrow
    5: "processing",
    6: "needs_email",
    7: "published",
    8: "processing(submitting)",  # text extraction , etc
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
