from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from modapi.db import get_db
from modapi.tables.arxiv_tables import arXiv_submission_flag
from modapi.tables.arxiv_models import SubmissionFlag, TapirUsers, Submissions
from modapi.rest.submission_filters import with_queue_filters

from sqlalchemy.sql import and_, select
from sqlalchemy.orm import joinedload, Session
from sqlalchemy.orm.attributes import instance_dict
from sqlalchemy import exc


from modapi.auth import User, auth_user

from . import schema

router = APIRouter()

query_options = [
    joinedload(SubmissionFlag.user)
    .joinedload(TapirUsers.username)
    .load_only("nickname")
]


@router.put("/submission/{submission_id}/flag")
async def put_flag(submission_id: int,
                   flag: schema.Flag,
                   user: User = Depends(auth_user),
                   db: Session = Depends(get_db)):
    """Puts a new flag on a submission"""
    try:
        stmt = arXiv_submission_flag.insert().values(
            user_id=user.user_id,
            flag=schema.modflag_to_int[flag.flag],
            submission_id=submission_id,
        )
        db.execute(stmt)
        db.commit()
        return 1
    except exc.IntegrityError:
        return JSONResponse(status_code=409,
                            content={"msg": "Flag already exists"})


@router.post("/submission/{submission_id}/flag/delete")
async def del_flag(submission_id: int,
                   user: User = Depends(auth_user),
                   db: Session = Depends(get_db)):
    # TODO check that the row actually gets deleted
    db.execute(
        arXiv_submission_flag.delete().where(
            and_(arXiv_submission_flag.c.submission_id == submission_id,
                 arXiv_submission_flag.c.user_id == user.user_id)
        )
    )
    db.commit()
    return 1


@router.get("/flags", response_model=List[schema.FlagOut])
async def flags(user: User = Depends(auth_user), db: Session = Depends(get_db)):
    """Gets list of submissions with flags.

    This is filtered to just flags on submissions a that mod or admin would
    have in thier queue.    
    """
    query = with_queue_filters(user, select(SubmissionFlag)
                               .options(*query_options)
                               .join(Submissions))
    res = db.execute(query).scalars().all()
    return list(map(_convert, res))


@router.get("/submission/{submission_id}/flag", response_model=List[schema.FlagOut])
async def get_flag(submission_id: int, user: User = Depends(auth_user),
                   db: Session = Depends(get_db)):
    """Get the flags for a single submission.

    Returns an empty list if there are no flags on the submission or
    the submission does not exist.

    This will return the flags regardless of the state of the
    submission.  It will return flags to moderators for papers
    outside their queue to support single submission view in the case
    the categories on the submision changed.
    """
    query = (select(SubmissionFlag)
             .options(*query_options)
             .filter(SubmissionFlag.submission_id == submission_id))
    return list(map(_convert, db.execute(query).scalars().all()))


def _convert(subFlag) -> schema.FlagOut:
    out = instance_dict(subFlag)
    out["username"] = subFlag.user.username.nickname
    return out
