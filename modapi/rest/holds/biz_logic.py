"""Routes for holds on submissions.

This works with the arXiv_submission_hold_reason table and is intended
to work for both mod and admin holds.

The paths in this module are intended to replace the /modhold paths.
"""

from typing import Union, List, Callable, Optional
from datetime import datetime
import pytz

from sqlalchemy.orm import Session
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse

from modapi.auth import User
from modapi.tables.arxiv_models import Submissions, SubmissionHoldReason

from .domain import HoldTypesIn, HoldLogicRes, HoldReleaseLogicRes,\
    SUBMITTED, WORKING, ON_HOLD


def hold_check(db: Session, submission_id: int):
    """Check for a hold.

    Returns None if no submission.

    Returns {status: int, user_id: int, reason: str} if submission exists and hold exists.

    Returns {status: int} if submission exists but hold doesn't exist
    in the hold table. This is might be a legacy style hold.

    """
    return db.query(Submissions).filter(Submissions.submission_id == submission_id).first()


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

    
    
def release_biz_logic(exists: Optional[Submissions], submission_id: int, user:
                      User, anno_time_fn:
                      Callable[[int],Union[datetime,int]]) -> Union[HoldReleaseLogicRes, JSONResponse]:
    if not user or (not user.is_admin and not user.is_moderator):
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN)
    
    if not exists:
        return JSONResponse(status_code=httpstatus.HTTP_404_NOT_FOUND,
                            content={"msg": "submission not found"})

    if exists.is_locked:  # This is hard locked, not an edit collab lock
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN,
                            content={"msg": "Submission is locked"})

    if exists.status != ON_HOLD:
        return JSONResponse(status_code=httpstatus.HTTP_409_CONFLICT,
                            content={"msg": "Submission is not on hold"})

    reasontype = exists.hold_reason.type if exists.hold_reason else None
    reasonreason = exists.hold_reason.reason if exists.hold_reason else None
    
    if not user.is_admin and user.is_moderator:
        if (exists.hold_reason is None or reasontype != "mod"):
            return JSONResponse(
                status_code=httpstatus.HTTP_403_FORBIDDEN,
                content={"msg": f"{submission_id} is not a mod hold"})

    if not exists.primary_classification:
        return JSONResponse(status_code=httpstatus.HTTP_409_CONFLICT,
                            content={"msg": "Submission cannot be released due to lack of a primary"})
        
    if reasontype:
        logtext = f'Release: {reasontype} {reasonreason} hold'
    else:
        logtext = "Release: legacy hold"

    rv = HoldReleaseLogicRes(
        modapi_comments=[logtext],
        visible_comments=[logtext],
        paper_id = exists.doc_paper_id or f"submit/{submission_id}",
        clear_reason = reasonreason,
        release_to_status = SUBMITTED if exists.submit_time else WORKING
    )

    if rv.release_to_status == SUBMITTED:
        now = datetime.now(tz=pytz.timezone('US/Eastern'))
        anno_time = anno_time_fn(submission_id)
        if now > anno_time:
            rv.set_release_time = now

    return rv


def _existing_type(exists: Submissions, shr: Optional[SubmissionHoldReason] )->str:
    if exists.status != ON_HOLD:
        return ''    
    if shr:
        return shr.type
    
def hold_biz_logic(hold: HoldTypesIn, exists: Optional[Submissions],
                   submission_id: int, user: User) -> Union[HoldLogicRes, JSONResponse]:
    if not user or (not user.is_admin and not user.is_moderator):
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN)
    
    if not exists:
        return JSONResponse(status_code=httpstatus.HTTP_404_NOT_FOUND,
                            content={"msg": "submission not found"})

    if exists.is_locked:  # This is hard locked, not an edit collab lock
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN,
                            content={"msg": f"{submission_id} is locked"})

    if not (exists.status in [1, 4, 2]):  # hold is included since some held subs can be held again
        return JSONResponse(status_code=httpstatus.HTTP_409_CONFLICT,
                            content={"msg": "Can only hold submissions in that status"})

    oldstat = status_by_number.get(exists.status, exists.status)
    rv = HoldLogicRes(
        modapi_comments=[f"Status changed from '{oldstat}' to 'on hold', reason: {hold.reason}"],
        visible_comments=_hold_comments(hold),
        paper_id = exists.doc_paper_id or f"submit/{submission_id}"
    )

    existing_reason = exists.hold_reason and exists.hold_reason.reason
    existing_type =  exists.hold_reason and exists.hold_reason.type
    if hold.type == 'mod':
        if existing_reason:
            # Mods cannot put a mod hold on a submission that is
            # already on admin or legacy hold. This is to avoid a
            # mod from changing a legacy hold to a mod-hold and
            # then that mod releaseing the hold. This would allow
            # a submission that is on hold for non-moderatorion
            # reasons such as copyright or failed TeX to
            # accidently get published.
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": "Mod hold on submission already exists"})
        elif exists.status == ON_HOLD:
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": "Hold on submission already exists"})
        else:
            rv.create_hold_reason = True

    elif hold.type == 'admin':
        if exists.status == ON_HOLD:
            if existing_type == "mod":
                rv.delete_hold_reason = True
                rv.create_hold_reason = True
                rv.visible_comments.insert(0, "Clear modhold, about to admin hold")
                rv.modapi_comments.insert(0, "Clear modhold")
            else:
                return JSONResponse(
                    status_code=httpstatus.HTTP_409_CONFLICT,
                    content={"msg": "Admin or legacy hold on submission already exists"})
            
        else: # not ON_HOLD
            if existing_type:
                return JSONResponse(
                    status_code=httpstatus.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"msg": "Submission not on hold but a hold reason exists"})
            else:
                rv.create_hold_reason = True
                
        # if exists.status != ON_HOLD and not existing_type:  # not on hold
        #     rv.create_hold_reason = True
        # elif exists.status == ON_HOLD and existing_type == "mod":  # on mod hold
        #     rv.delete_hold_reason = True
        #     rv.create_hold_reason = True
        #     rv.visible_comments.insert(0, "Clear modhold, about to admin hold")
        #     rv.modapi_comments.insert(0, "Clear modhold")
        # else:
        #     return JSONResponse(
        #         status_code=httpstatus.HTTP_409_CONFLICT,
        #         content={"msg": "Admin hold on submission already exists"})
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
