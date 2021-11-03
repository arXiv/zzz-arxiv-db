"""Routes for category rejections on submissions."""
import re

from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from modapi.auth import User, auth_user
from modapi.db import get_db
from modapi.tables.arxiv_tables import (
    arXiv_submissions,
    arXiv_submission_category,
    arXiv_submission_category_proposal,
)

from modapi.tables.arxiv_models import Submissions, AdminLog
from modapi.email import build_reject_cross_email, send_email
from ..holds.domain import SUBMITTED, ON_HOLD, NEXT

from .. import schema

import logging

log = logging.getLogger(__name__)

router = APIRouter()

REMOVED = 9
"""Submission table status for removed."""

SYSTEM_USER_ID = 1
"""Internal ID for system user."""

PROPOSAL_STATUS_ACCEPTED_AS_SECONDARY = 2
PROPOSAL_STATUS_REJECTED = 3


@router.post("/submission/{submission_id}/category_rejection")
async def category_rejection(
    submission_id: int,
    rejection: schema.CategoryRejection,
    user: User = Depends(auth_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Reject a single category from a submission.

    If the submission is of type `new`:
    - If the category being rejected is a primary, remove the category from the
    submission, put the submission on hold, and log the action to the admin
    log.
    - If the category is a secondary, remove it from the submission and log
    the action.
    - If the category is a primary as the action is "accept_secondary", update
    the category to become a secondary and log the action.

    If submission is of type `cross`:
    - If the category being rejected is the only category in the set of new
    "cross" categories, set the submission status to REMOVED (9), log the
    action to the admin log and notify the
    submitter via email.
    - If the category is one of multiple categories in the set of new "cross"
    categories, remove the category from the submission
    and log the action to the admin log.

    Returns "success" if the category_rejection completed successfully.
    """
    submission = _active_submission_check(db, submission_id)
    if not submission:
        return JSONResponse(status_code=404)
    if submission.is_locked:
        return JSONResponse(status_code=403)
    unpublished_secondaries = submission.new_crosses

    if submission.type == "cross" and rejection.action == "reject":
        do_send_email = False

        if rejection.category in unpublished_secondaries:
            logtext = f"rejected {rejection.category} from cross"
            if len(unpublished_secondaries) > 1:
                # remove the category
                stmt = arXiv_submission_category.delete().where(
                    and_(
                        arXiv_submission_category.c.submission_id == submission_id,
                        arXiv_submission_category.c.is_primary == 0,
                        arXiv_submission_category.c.category == rejection.category,
                    )
                )
                db.execute(stmt)
            else:
                submission.status = REMOVED
                logtext = logtext + "; removed submission"
                do_send_email = True

            admin_log = AdminLog(
                submission_id=submission_id,
                paper_id=submission.doc_paper_id,
                username=user.username,
                program="modapi.rest",
                command="admin comment",
                logtext=logtext,
            )
            db.add(admin_log)
            db.commit()
        else:
            return JSONResponse(status_code=409)

        if do_send_email:
            msg = build_reject_cross_email(
                submission.submitter_email, [rejection.category]
            )
            send_email(msg)
    elif submission.type == "new" and rejection.action in (
        "reject",
        "accept_secondary",
    ):

        if rejection.category == submission.primary_classification:
            is_primary = True
        elif rejection.category in unpublished_secondaries:
            is_primary = False
        else:
            return JSONResponse(status_code=409)

        original_cats = _get_category_str(submission)
        was_held = False

        if is_primary and submission.status in [SUBMITTED, NEXT]:
            # put on hold
            stmt = (
                arXiv_submissions.update()
                .values(status=ON_HOLD)
                .where(arXiv_submissions.c.submission_id == submission_id)
            )
            db.execute(stmt)
            was_held = True

        if rejection.action == "reject":
            stmt = arXiv_submission_category.delete().where(
                and_(
                    arXiv_submission_category.c.submission_id == submission_id,
                    arXiv_submission_category.c.is_primary == int(is_primary),
                    arXiv_submission_category.c.category == rejection.category,
                )
            )
            db.execute(stmt)
            db.commit()

            _log_and_propose_rejection(
                db=db,
                submission=submission,
                user=user,
                rejection=rejection,
                is_primary=is_primary,
                was_held=was_held,
                rejection_msg=f"{original_cats} => {_get_category_str(submission)}",
            )
        elif rejection.action == "accept_secondary" and is_primary:
            # change primary to secondary
            stmt = (
                arXiv_submission_category.update()
                .values(is_primary=0)
                .where(
                    and_(
                        arXiv_submission_category.c.submission_id == submission_id,
                        arXiv_submission_category.c.is_primary == 1,
                        arXiv_submission_category.c.category == rejection.category,
                    )
                )
            )
            db.execute(stmt)
            db.commit()

            _log_and_propose_rejection(
                db=db,
                submission=submission,
                user=user,
                rejection=rejection,
                is_primary=is_primary,
                was_held=was_held,
                rejection_msg=f"{original_cats} => {_get_category_str(submission)}",
            )
        else:
            return JSONResponse(status_code=409)
    else:
        return JSONResponse(status_code=403)

    return "success"


def _active_submission_check(db: Session, submission_id: int):
    """Check whether submission_id is an active cross."""
    return (
        db.query(Submissions)
        .filter(
            Submissions.submission_id == submission_id,
            Submissions.status.in_([SUBMITTED, ON_HOLD, NEXT]),
        )
        .first()
    )


def _get_category_str(submission: Submissions) -> str:
    """Get category string used in logs."""
    cat_str = submission.fudged_categories
    if cat_str == "-":
        cat_str = "none"
    else:
        cat_str = re.sub(r"^-", "no primary", cat_str)
    return cat_str


def _log_and_propose_rejection(
    db: Session,
    submission: Submissions,
    user: User,
    rejection: schema.CategoryRejection,
    is_primary: bool,
    was_held: bool,
    rejection_msg: str,
    comment: str = None,
) -> None:
    """Log action to admin comment log and create resolved proposal."""
    # Build the admin comment
    msg = f"Rejected category {rejection.category} as "
    if is_primary:
        msg = msg + "primary"
        if rejection.action == "accept_secondary":
            msg = msg + ", accepted it as secondary"
    else:
        msg = msg + "secondary"
    msg = msg + (" and put on Hold" if was_held else "")
    msg = msg + (f"; {rejection_msg}")
    msg = msg + (f": {comment}" if comment else "")

    admin_log = AdminLog(
        submission_id=submission.submission_id,
        paper_id=submission.doc_paper_id,
        username=user.username,
        program="modapi.rest",
        command="admin comment",
        logtext=msg,
    )
    db.add(admin_log)
    db.commit()

    # Build the insert statement for an entry into the proposal table.
    proposal_status = (
        PROPOSAL_STATUS_REJECTED
        if rejection.action == "reject"
        else PROPOSAL_STATUS_ACCEPTED_AS_SECONDARY
    )
    stmt = arXiv_submission_category_proposal.insert().values(
        submission_id=submission.submission_id,
        category=rejection.category,
        is_primary=int(is_primary),
        user_id=user.user_id,
        proposal_status=proposal_status,
        updated=func.now(),
        proposal_comment_id=admin_log.id,
    )
    db.execute(stmt)
    db.commit()
