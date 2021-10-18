"""Routes for category rejections on submissions."""
from typing import Union, List, Optional

from sqlalchemy import select, or_, and_, null
from sqlalchemy.orm import joinedload, Session
from fastapi import APIRouter, Depends
from pydantic import conlist
from fastapi.responses import JSONResponse

from modapi.auth import User, auth_user
from modapi.db import get_db
from modapi.tables.arxiv_tables import arXiv_admin_log, arXiv_submissions

from modapi.tables.arxiv_models import Submissions
from modapi.tables.arxiv_tables import arXiv_submission_category, arXiv_admin_log
from .biz_logic import cross_categories, active_cross_check

from .. import schema

import logging

log = logging.getLogger(__name__)


router = APIRouter()

REMOVED = 9
"""Submission table status for removed."""


@router.post("/submission/{submission_id}/reject_cross")
async def reject_cross(
    submission_id: int,
    category: schema.CrossRejection,
    user: User = Depends(auth_user),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """Reject a single category from a submission of type `cross`.

    If the category being rejected is the only category in the set of new
    "cross" categories, set the submission status to REMOVED (9), log the
    action to the admin log and notify the
    submitter via email.

    If the category is one of many categories in the set of new "cross"
    categories, remove the category from the submission
    and log the action to the admin log.
    """
    submission = active_cross_check(db, submission_id)
    if not submission:
        return JSONResponse(status_code=404)
    cross_cats = submission.new_crosses
    send_email = False

    if cross_cats and category.category in cross_cats:
        logtext = f"rejected {category.category} from cross"
        if len(cross_cats) > 1:
            # remove the category
            stmt = arXiv_submission_category.delete().where(
                and_(
                    arXiv_submission_category.c.submission_id == submission_id,
                    arXiv_submission_category.c.is_primary == 0,
                    arXiv_submission_category.c.category == category.category,
                )
            )
            db.execute(stmt)
        else:
            submission.status = REMOVED
            logtext = logtext + "; removed submission"
            send_email = True

        stmt = arXiv_admin_log.insert().values(
            submission_id=submission_id, paper_id=submission.doc_paper_id, username=user.username,
            program="modapi.rest", command="reject_cross", logtext=logtext)
        db.execute(stmt)
        db.commit()
    else:
        return JSONResponse(status_code=409)

    # TODO: email
    if send_email:
        pass

    return 1
