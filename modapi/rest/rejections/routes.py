"""Routes for category rejections on submissions."""
import smtplib
from typing import Union, List, Optional

from sqlalchemy import select, and_, null
from sqlalchemy.orm import joinedload, Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from modapi.config import config
from modapi.auth import User, auth_user
from modapi.db import get_db
from modapi.tables.arxiv_tables import arXiv_admin_log, arXiv_submissions

from modapi.tables.arxiv_models import Submissions
from modapi.tables.arxiv_tables import arXiv_submission_category, arXiv_admin_log
from modapi.email import build_reject_cross_email, send_email
from ..holds.domain import SUBMITTED, ON_HOLD, NEXT
from .biz_logic import active_submission_check

from .. import schema

import logging

log = logging.getLogger(__name__)


router = APIRouter()

REMOVED = 9
"""Submission table status for removed."""


@router.post("/submission/{submission_id}/category_rejection")
async def category_rejection(
    submission_id: int,
    rejection: schema.CategoryRejection,
    user: User = Depends(auth_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Reject a single category from a submission.

    If the submission is of type `new`:
    TBD

    If submission is of type `cross`:
    - If the category being rejected is the only category in the set of new
    "cross" categories, set the submission status to REMOVED (9), log the
    action to the admin log and notify the
    submitter via email.
    - If the category is one of many categories in the set of new "cross"
    categories, remove the category from the submission
    and log the action to the admin log.
    """
    submission = active_submission_check(db, submission_id)
    if not submission:
        return JSONResponse(status_code=404)
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

            stmt = arXiv_admin_log.insert().values(
                submission_id=submission_id,
                paper_id=submission.doc_paper_id,
                username=user.username,
                program="modapi.rest",
                command="reject_cross",
                logtext=logtext,
            )
            db.execute(stmt)
            db.commit()
        else:
            return JSONResponse(status_code=409)

        if do_send_email:
            msg = build_reject_cross_email(
                submission.submitter_email, [rejection.category]
            )
            send_email(msg)
    elif submission.type == "new":

        # TODO:
        # if valid category, remove
        # if category was primary
        #   put on hold
        # if category was secondary no need for hold
        # remove the category
        if rejection.category == submission.primary_classification:
            is_primary = True
        elif rejection.category in unpublished_secondaries:
            is_primary = False
        else:
            return JSONResponse(status_code=409)

        if is_primary and submission.status in [SUBMITTED, NEXT]:
            # put on hold
            stmt = (arXiv_submissions.update()
                    .values(status=ON_HOLD)
                    .where(arXiv_submissions.c.submission_id == submission_id))
            db.execute(stmt)
            # log old/new status?

        stmt = arXiv_submission_category.delete().where(
            and_(
                arXiv_submission_category.c.submission_id == submission_id,
                arXiv_submission_category.c.is_primary == int(is_primary),
                arXiv_submission_category.c.category == rejection.category,
            )
        )
        db.execute(stmt)
        # log action
        # log as proposal?
        db.commit()
        pass
    else:
        return JSONResponse(status_code=403)

    return 1
