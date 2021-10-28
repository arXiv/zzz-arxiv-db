"""Business logic for category rejections."""

from typing import Union, List, Callable, Optional

from sqlalchemy.orm import Session
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse

from ..holds.domain import SUBMITTED, WORKING, ON_HOLD, NEXT

from modapi.auth import User
from modapi.tables.arxiv_models import Submissions
from modapi.tables.arxiv_tables import arXiv_submission_category

def cross_categories(db: Session, submission_id) -> Optional[List]:
    """Get the categories associated with a cross."""
    exists = active_cross_check(db, submission_id)
    if not exists:
        return None
    return exists.new_crosses


def active_cross_check(db: Session, submission_id):
    """Check whether submission_id is an active cross."""
    return db.query(Submissions).filter(Submissions.submission_id == submission_id,
                                        Submissions.type == "cross",
                                        Submissions.status.in_([SUBMITTED, ON_HOLD, NEXT])).first()
