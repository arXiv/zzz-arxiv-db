"""Routes for holds on submissions.

This works with the arXiv_submission_hold_reason table and is intended
to work for both mod and admin holds.

The paths in this module are intended to replace the /modhold paths.
"""

from modapi.rest.earliest_announce import earliest_announce
from typing import Union, List, Callable, Optional
from datetime import datetime, timedelta
import pytz


from sqlalchemy.orm import Session
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse

from modapi.auth import User
from modapi.tables.arxiv_models import Submissions

from .domain import (
    HoldTypesIn,
    HoldLogicRes,
    HoldReleaseLogicRes,
    SUBMITTED,
    WORKING,
    ON_HOLD,
    NEXT,
)


def hold_check(db: Session, submission_id: int):
    """Check for a hold.

    Returns None if no submission.

    Returns {status: int, user_id: int, reason: str} if submission exists and hold exists.

    Returns {status: int} if submission exists but hold doesn't exist
    in the hold table. This is might be a legacy style hold.

    """
    return (
        db.query(Submissions).filter(Submissions.submission_id == submission_id).first()
    )


def _hold_comments(hold: HoldTypesIn) -> List[str]:
    """Returns a list of comments that should be stored in the admin log in order
    in a way that will be visible to admins and mods."""
    if hold.type == "mod":
        return [f"Mod Hold reason: {hold.reason}"]
    elif hold.type == "admin":
        if hold.reason == "other":
            return [
                "Admin Hold for reason: other. "
                f"sendback: {str(hold.sendback)} comment: {hold.comment}"
            ]
        elif hold.reason == "reject-other":
            return [
                "Admin Hold and Reject for reason: reject-other"
                f" with comment: {hold.comment}"
            ]
        else:
            return [f"Admin Hold and Reject for reason: {hold.reason}"]
    else:
        return [f"Hold of type {hold.type}"]


def release_by_mod_biz_logic(
    exists: Optional[Submissions],
    submission_id: int,
    user: User,
    anno_time_fn: Callable[[int], datetime],
    is_freeze: bool
) -> Union[HoldReleaseLogicRes, JSONResponse]:
    """Hold logic for moderator users"""
    if not user or (not user.is_admin and not user.is_moderator):
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN)
    if not exists:
        return JSONResponse(
            status_code=httpstatus.HTTP_404_NOT_FOUND,
            content={"msg": "submission not found"},
        )
    if exists.is_locked:  # This is hard locked, not an edit collab lock
        return JSONResponse(
            status_code=httpstatus.HTTP_403_FORBIDDEN,
            content={"msg": "Submission is locked"},
        )
    if exists.status != ON_HOLD:
        return JSONResponse(
            status_code=httpstatus.HTTP_409_CONFLICT,
            content={"msg": "Submission is not on hold"},
        )

    reasontype = exists.hold_reason.type if exists.hold_reason else "legacy"
    reasonreason = f" {exists.hold_reason.reason}" if exists.hold_reason else ""

    if not user.is_admin and user.is_moderator:
        if exists.hold_reason is None or reasontype != "mod":
            return JSONResponse(
                status_code=httpstatus.HTTP_403_FORBIDDEN,
                content={"msg": f"{submission_id} is not a mod hold"},
            )
    if not exists.primary_classification:
        return JSONResponse(
            status_code=httpstatus.HTTP_409_CONFLICT,
            content={"msg": "Submission cannot be released due to lack of a primary"},
        )

    if exists.auto_hold:
        new_status = 2  # admins need to release auto hold to retrigger checks in legacy
        logtext = [f"Release: {reasontype}{reasonreason} hold",
                   f"Hold: {reasontype}{reasonreason} cleared but submission was on auto-hold "+\
                   "and needs to be cleared by admins" ]
    else:
        submitted_by_user = exists.submit_time
        new_status =(WORKING if not submitted_by_user
                     else NEXT if is_freeze
                     else SUBMITTED)
        logtext = [f"Release: {reasontype}{reasonreason} hold to {status_by_number[new_status]}"]
        
    rv = HoldReleaseLogicRes(
        modapi_comments=logtext,
        visible_comments=logtext,
        paper_id=exists.doc_paper_id or f"submit/{submission_id}",
        clear_reason=bool(reasonreason),
        release_to_status=new_status
    )

    """ This code snippet implements the logic from here:
    https://github.com/arXiv/arxiv-lib/blob/fa9cf336b81dbea4428233ec081feb7b0a4c1b9e/lib/arXiv/Schema/Result/Submission.pm#L2810

        # Release time is used to determine order of paper_id assignment for
        # held submissions, so that they don't show up at the top of the
        # list. In the case of things held and released in the same day,
        # we don't want to change the order
    """
    if rv.release_to_status in (SUBMITTED, NEXT):
        now = datetime.now(tz=pytz.timezone("US/Eastern"))
        earliest_possible_anno_time = anno_time_fn(submission_id)
        if now > earliest_possible_anno_time:
            rv.set_release_time = now

    return rv


def hold_biz_logic(
    hold: HoldTypesIn, exists: Optional[Submissions], submission_id: int, user: User
) -> Union[HoldLogicRes, JSONResponse]:
    if not user or (not user.is_admin and not user.is_moderator):
        return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN)

    if not exists:
        return JSONResponse(
            status_code=httpstatus.HTTP_404_NOT_FOUND,
            content={"msg": "submission not found"},
        )

    if exists.is_locked:  # This is hard locked, not an edit collab lock
        return JSONResponse(
            status_code=httpstatus.HTTP_403_FORBIDDEN,
            content={"msg": f"{submission_id} is locked"},
        )

    if not (
        exists.status in [SUBMITTED, NEXT, ON_HOLD]
    ):  # hold is included for legacy_hold -> new_style_hold
        return JSONResponse(
            status_code=httpstatus.HTTP_409_CONFLICT,
            content={"msg": "Submission in status that does not allow hold"},
        )

    oldstat = status_by_number.get(exists.status, exists.status)
    rv = HoldLogicRes(
        modapi_comments=[
            f"Status changed from '{oldstat}' to 'on hold', reason: {hold.reason}"
        ],
        visible_comments=_hold_comments(hold),
        paper_id=exists.doc_paper_id or f"submit/{submission_id}",
    )

    existing_reason = exists.hold_reason and exists.hold_reason.reason
    existing_type = (exists.hold_reason and exists.hold_reason.type) or "legacy"
    if hold.type == "mod":
        if exists.status == ON_HOLD:
            # Mods cannot put a mod hold on a submission that is already on
            # admin or legacy hold. This is to avoid a mod from changing a
            # legacy hold to a mod-hold and then that mod releaseing the
            # hold. This would allow a submission that is on hold for
            # non-moderatorion reasons such as copyright or failed TeX to
            # accidently get published.
            return JSONResponse(
                status_code=httpstatus.HTTP_409_CONFLICT,
                content={"msg": "Hold on submission already exists"},
            )
        elif existing_reason:
            # This is a case that should not exist, if there is a hold reason,
            # the submission should be on hold. Roll with it.
            rv.create_hold_reason = True
            rv.delete_hold_reason = True
            rv.visible_comments.insert(
                0, "Clear lingering {existing_type} hold, about to mod hold"
            )
            rv.modapi_comments.insert(0, "Clear {existing_type} hold")
        else:
            rv.create_hold_reason = True

    elif hold.type == "admin":
        if exists.status == ON_HOLD:
            if existing_reason and existing_type == "mod":
                rv.delete_hold_reason = True
                rv.create_hold_reason = True
                rv.visible_comments.insert(0, "Clear mod hold, about to admin hold")
                rv.modapi_comments.insert(0, "Clear mod hold")
            elif existing_type == "legacy":
                rv.create_hold_reason = True
            else:
                return JSONResponse(
                    status_code=httpstatus.HTTP_409_CONFLICT,
                    content={
                        "msg": f"{existing_type} hold on submission already exists"
                    },
                )

        else:  # type admin but not ON_HOLD
            if existing_reason:
                # This is a case that should not exist, if there is a
                # hold in the hold reasons, the submission should be
                # on hold. But submissions can get into this state due
                # to the submitter putting a submision on 'working', and
                # then back to 'submitted'.
                #
                # The clear intent of the mod/admin is to put this submission on hold,
                # so try to put it on hold.
                rv.create_hold_reason = True
                rv.delete_hold_reason = True
                rv.visible_comments.insert(
                    0, "Clear lingering {existing_type}, about to admin hold"
                )
                rv.modapi_comments.insert(0, "Clear {existing_type}")
            else:
                rv.create_hold_reason = True

    else:
        return JSONResponse(   # pragma: no cover
            status_code=httpstatus.HTTP_400_BAD_REQUEST,
            content={"msg": "invalid hold type"},
        )

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
    20: "deleted(working)",  # was working but expired
    22: "deleted(on hold)",
    25: "deleted(processing)",
    27: "deleted(published)",  # published and files expired
    29: "deleted(removed)",
    30: "deleted(user deleted)",  # user deleted and files expired
}
