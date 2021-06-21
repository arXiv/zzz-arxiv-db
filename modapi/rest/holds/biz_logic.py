"""Routes for holds on submissions.

This works with the arXiv_submission_hold_reason table and is intended
to work for both mod and admin holds.

The paths in this module are intended to replace the /modhold paths.
"""

from typing import Union, List, Callable
from datetime import datetime
import pytz

from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse

from modapi.auth import User

from .domain import HoldTypesIn, HoldLogicRes, HoldReleaseLogicRes,\
    SUBMITTED, WORKING, ON_HOLD

import logging
log = logging.getLogger(__name__)


def hold_check(db: Session, submission_id: int):
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
        s.status, shr.reason, shr.user_id, shr.type, s.submit_time, s.sticky_status, s.is_locked, docs.paper_id
        FROM
        arXiv_submissions s LEFT JOIN arXiv_submission_hold_reason shr
        ON s.submission_id = shr.submission_id
        LEFT JOIN arXiv_documents docs
        ON s.document_id = docs.document_id
        WHERE s.submission_id = :submission_id
        """),
        {"submission_id": submission_id},
    )
    sub = res.first()
    if sub:
        [status, reason, hold_user_id, hold_type, submit_time, sticky_status, is_locked, paper_id] = sub
        log.debug('For sub %d hold_check was type: %s status: %s reason: %s sticky_status: %s is_locked: %s submit_time %s paper_id: %s',
                  submission_id, hold_type, status, reason, sticky_status, is_locked, submit_time, paper_id)
        return sub
    else:
        return None


def _hold_comments(hold: HoldTypesIn) -> List[str]:
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

    
    
def release_biz_logic(exists, submission_id: int, user: User, anno_time_fn: Callable[[int],Union[datetime,int]]) -> Union[HoldReleaseLogicRes, JSONResponse]:
    if not user or (not user.is_admin and not user.is_moderator):
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN)
    
    if not exists:
        return JSONResponse(status_code=httpstatus.HTTP_404_NOT_FOUND,
                            content={"msg": "submission not found"})

    if exists["is_locked"]:  # This is hard locked, not an edit collab lock
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN,
                            content={"msg": "Submission is locked"})

    if not user.is_admin and user.is_moderator:
        if (exists["type"] != "mod" or exists["reason"] is None):
            return JSONResponse(
                status_code=httpstatus.HTTP_403_FORBIDDEN,
                content={"msg": f"{submission_id} is not a mod hold"})

    if exists["type"] is not None:
        logtext = f'Release: {exists["type"]} {exists["reason"]} hold'
    else:
        logtext = "Release: legacy hold"

    rv = HoldReleaseLogicRes(
        modapi_comments=[logtext],
        visible_comments=[logtext],
        paper_id = exists["paper_id"] or f"submit/{submission_id}",
        clear_reason = exists["reason"],
        release_to_status = SUBMITTED if exists["submit_time"] else WORKING
    )

    if rv.release_to_status == SUBMITTED:
        now = datetime.now(tz=pytz.timezone('US/Eastern'))
        anno_time = anno_time_fn(submission_id)
        if now > anno_time:
            rv.set_release_time = now

    return rv
    
def hold_biz_logic(hold: HoldTypesIn, exists, submission_id: int, user: User) -> Union[HoldLogicRes, JSONResponse]:
    if not user or (not user.is_admin and not user.is_moderator):
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN)
    
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
        visible_comments=_hold_comments(hold),
        paper_id = exists["paper_id"] or f"submit/{submission_id}"
    )

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
