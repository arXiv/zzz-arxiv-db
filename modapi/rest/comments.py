from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from modapi.db import get_db
from modapi.tables.arxiv_tables import arXiv_submission_flag
from modapi.tables.arxiv_models import SubmissionFlag, TapirUsers, Submissions, AdminLog
from modapi.rest.submission_filters import with_queue_filters

from sqlalchemy.sql import and_, select
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.orm.attributes import instance_dict

from pydantic import BaseModel

from modapi.auth import User, auth_user

from . import schema

router = APIRouter()

query_options = [
    joinedload(SubmissionFlag.user)
    .joinedload(TapirUsers.username)
    .load_only("nickname")
]

class CommentIn(BaseModel):
    comment: str


@router.post("/submission/{submission_id}/comment")
async def post_comment(submission_id: int,
                       comment_data: CommentIn,
                       user: User = Depends(auth_user),
                       db: Session = Depends(get_db)):
    """Adds a new comment on a submission"""
    # TODO check that the submission exists

    sub = db.query(Submissions).filter(Submissions.submission_id == submission_id).first()
    if not sub:
        return JSONResponse(status_code=httpstatus.HTTP_404_NOT_FOUND,
                            content={"msg":"Submission not found"})

    if sub.is_locked:
            return JSONResponse(status_code=httpstatus.HTTP_403_FORBIDDEN,
                            content={"msg": "Submission is locked"})

    paper_id = sub.doc_paper_id or f"submit/{submission_id}"

    # TODO Need to do something like holds/buz_logic with paper_id and hard lock
    comment = AdminLog(submission_id= submission_id,
                       paper_id=paper_id,
                       username=user.username,
                       program='Admin::Queue',
                       command='admin comment',
                       logtext=comment_data.comment)
    db.add(comment)
    db.commit()    
    return 1


@router.get("/submission/{submission_id}/comments", response_model=List[schema.Comment])
async def get_comments(user: User = Depends(auth_user),
                       db: Session = Depends(get_db)):
    """Gets a list of comments on the submission."""
    pass
    # query = with_queue_filters(user, select(SubmissionFlag)
    #                            .options(*query_options)
    #                            .join(Submissions))
    # res = db.execute(query).scalars().all()
    #return list(map(_convert, res))



def _convert(subFlag) -> schema.FlagOut:
    out = instance_dict(subFlag)
    out["username"] = subFlag.user.username.nickname
    return out

