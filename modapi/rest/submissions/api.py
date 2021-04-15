from typing import List

# from modapi.collab.collab_app import sio
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy import select, or_, and_
from sqlalchemy.orm import joinedload

from modapi.auth import auth_user, User
from modapi.db import Session
from modapi.rest import schema

# from .models import SubmissionsOut

from modapi.db.arxiv_models import (
    Submissions,
    TapirUsers,
    Demographics,
    CategoryDef,
    SubmissionCategory,
    SubmissionCategoryProposal,
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
    .joinedload(TapirUsers.demographics)
    .load_only("flag_suspect"),
    joinedload(Submissions.abs_classifier_data).load_only("json"),
    joinedload(Submissions.proposals),
    joinedload(Submissions.hold_reasons),
    joinedload(Submissions.flags),
]


@router.get("/submissions", response_model=List[schema.Submission])
async def submissions(user: User = Depends(auth_user)):
    """Get all submissions for moderator or admin"""
    async with Session() as session:
        stmt = (
            select(Submissions)
            .outerjoin(Submissions.submission_category)
            .outerjoin(SubmissionCategory.arXiv_category_def)
            .outerjoin(Submissions.proposals)
            .options(*query_options)
            .filter(Submissions.status.in_([1, 2, 4]))
            )

        if user.is_moderator and not user.is_admin:
            mods_categories = user.moderated_categories
            category_ors = [
                SubmissionCategory.category.in_(mods_categories),
                and_(
                    SubmissionCategoryProposal.category.in_(mods_categories),
                    SubmissionCategoryProposal.proposal_status == 0,
                ),
            ]
            for archive in user.moderated_archives:
                category_ors.append(
                    SubmissionCategory.category.startswith(archive))
                # modui2 excluded subs with proposals in mod's archive
                # category_ors.append(
                #     and_(
                #         SubmissionCategoryProposal.category.startswith(archive),
                #         SubmissionCategoryProposal.proposal_status == 0)
                #     )
            stmt = stmt.filter(Submissions.type.in_(['new','rep','cross']))
            stmt = stmt.filter(or_(*category_ors))

        res = await session.execute(stmt)
        rows = res.unique().all()
        return [to_submission(row[0]) for row in rows]


@router.get("/submission/{submission_id}", response_model=schema.Submission)
async def submission(submission_id: int, user: User = Depends(auth_user)):
    """Gets a submission"""
    async with Session() as session:
        stmt = (
            select(Submissions)
            .options(*query_options)
            .where(Submissions.submission_id == submission_id)
        )
        res = await session.execute(stmt)

        row = res.unique().fetchone()
        if row:
            return to_submission(row[0])
        else:
            return JSONResponse(
                status_code=404,
                content={"msg": "submission not found"}
            )
