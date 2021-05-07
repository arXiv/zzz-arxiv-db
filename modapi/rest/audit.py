"""API endpoints to facilitate testing by providing unfiltered results"""



from typing import Optional, Union, List

from fastapi import APIRouter, Depends
from modapi.auth import User, auth_user
from modapi.db import Session
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

from sqlalchemy import select, or_, and_, text
from sqlalchemy.orm import joinedload


router = APIRouter()


@router.get("/testing/submissions")
async def submissions(user: User = Depends(auth_user)):
    """Returns minimal data for all the active submissions

    { subid: 1234, status: 1|2|4 , proposals: [], categories: [], hold_reaons: ["mod"|"admin", "reason"] }

    The idea here is that we can write a integration test that gets
    the testing_submissions data, and then gets the /submissions data
    for a user. Then the unfiltered testing_submissions data can be
    compared with the filtered for the logged in mod /submissions data.

    This should return minimal data that is just enough to confirm
    proper filtering. It should only return submission ids,
    categories, proposals. It shouldn't return authors, titles
    abstracts etc.

    """
    def proposal_cats(sub: Submissions):
        if not sub.proposals:
            return []
        else:
            return [prop.category for prop in sub.proposals if prop.proposal_status == 0]

    def cats(sub: Submissions):
        return [ cat.category for cat in sub.submission_category ]

    def hold_reasons(sub: Submissions):
        if sub.hold_reasons:
            return {"type": sub.hold_reasons[0].type, "reason": sub.hold_reasons[0].reason}

    query_options = [
        joinedload(Submissions.submission_category),
        joinedload(Submissions.proposals),
        joinedload(Submissions.hold_reasons),
    ]

    async with Session() as session:
        stmt = (select(Submissions)
                .options(*query_options)
                .filter(Submissions.status.in_([1, 2, 4]))
                        )
        res = await session.execute(stmt)
        out = []
        for row in res.unique():
            sub = row[0]
            data = dict(sub_id=sub.submission_id,
                        status=sub.status,
                        proposal_cats=proposal_cats(sub),
                        cats=cats(sub),
                        hold_reasons=hold_reasons(sub))                
            out.append(data)
        
        return out


@router.get("/testing/holds")
async def holds(user: User = Depends(auth_user)):
    async with Session() as session:
        stmt = (select(Submissions)
                .options(joinedload(Submissions.hold_reasons))
                .filter(Submissions.status == 2)
                )
        res = await session.execute(stmt)
        out = []
        for row in res.unique():
            sub = row[0]
            if sub.hold_reasons:
                out.append([int(sub.submission_id),
                            sub.hold_reasons[0].type,
                            sub.hold_reasons[0].reason])
            else:
                out.append([int(sub.submission_id), 'legacy'])

        return out

