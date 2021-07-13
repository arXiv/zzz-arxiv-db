from typing import List, Optional

# from modapi.collab.collab_app import sio
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import select, or_, and_, func, literal
from sqlalchemy.orm import joinedload, Session

from modapi.auth import auth_user, User
from modapi.db import get_db
from modapi.rest import schema
from modapi.rest.submission_filters import with_queue_filters

from modapi.tables.arxiv_models import (
    Submissions,
    TapirUsers,
    Demographics,
    CategoryDef,
    SubmissionCategory,
    SubmissionCategoryProposal,
    AdminLog,
)

from .convert import to_submission

router = APIRouter(
   dependencies=[Depends(auth_user)]
)

# Options to for that are needed to bring in all the
# values that are used for the ORM queries.
#
# The joinedload() objects will configure SQLA to load the table
# during the initial query using a join. The load_only part will restrict the
# loaded columns to only a limited set of columns.
#
# May need to go to other types of loads than joins if there are
# peformance problems.
# https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html
query_options = [
    joinedload(Submissions.submission_category),
    joinedload(Submissions.submitter).joinedload(TapirUsers.username),
    joinedload(Submissions.submitter)
    .joinedload(TapirUsers.demographics).load_only("flag_suspect"),
    joinedload(Submissions.abs_classifier_data).load_only("json"),
    joinedload(Submissions.proposals),
    joinedload(Submissions.hold_reasons),
    joinedload(Submissions.admin_log).load_only(AdminLog.id, AdminLog.command),
    joinedload(Submissions.flags),
]


def _query(user: User, include_mod_archives: bool, exclude_mod_categories: bool):
    """Builds a query to select submissons"""
    stmt = select(Submissions).options(*query_options)
    return with_queue_filters(user, stmt, include_mod_archives, exclude_mod_categories)


@router.get("/submissions", response_model=List[schema.Submission])
async def submissions(user: User = Depends(auth_user),
                      db: Session = Depends(get_db),
                      include_mod_archives: bool = True,
                      exclude_mod_categories: bool = False):
    """Get all submissions for moderator or admin

    Moderators will be limited to just submissions in their categories
    or archives queues.
    """
    rows = db.execute(_query(user, include_mod_archives, exclude_mod_categories)).unique().all()
    return [to_submission(row[0], user) for row in rows]


@router.get("/submission/{submission_id}", response_model=schema.Submission)
async def submission(submission_id: int, user: User = Depends(auth_user),
                     db: Session = Depends(get_db)):
    """Gets a single submission."""
    res = db.execute(select(Submissions)
                     .options(*query_options)
                     .where(Submissions.submission_id == submission_id))
    row = res.unique().fetchone()
    if row:
        return to_submission(row[0], user)
    else:
        return JSONResponse(status_code=404,
                            content={"msg": "submission not found"})
