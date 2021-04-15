from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from modapi.db import engine
from modapi.db.arxiv_tables import arXiv_submission_flag, tapir_nicknames
from sqlalchemy.sql import and_, select
from sqlalchemy import exc

from modapi.auth import User, auth_user

from . import schema

router = APIRouter()


@router.put("/submission/{submission_id}/flag")
async def put_flag(submission_id: int,
                   flag: schema.ModFlag,
                   user: User = Depends(auth_user)):
    async with engine.begin() as conn:
        try:
            stmt = arXiv_submission_flag.insert().values(
                user_id=user.user_id,
                flag=schema.modflag_to_int[flag.flag],
                submission_id=submission_id,
            )
            await conn.execute(stmt)
        except exc.IntegrityError:
            return JSONResponse(status_code=409,
                                content={"msg": "Flag already exists"})


@router.post("/submission/{submission_id}/flag/delete")
async def del_flag(submission_id: int,
                   user: User = Depends(auth_user)):
    # TODO check that the row actually gets deleted
    async with engine.begin() as conn:
        await conn.execute(
            arXiv_submission_flag.delete().where(
                and_(
                    arXiv_submission_flag.c.submission_id == submission_id,
                    arXiv_submission_flag.c.user_id == user.user_id
                )
            )
        )


@router.get("/flags", response_model=List[schema.ModFlagOut])
async def flags(user: User = Depends(auth_user)):
    """Gets list of submissions with checkmarks"""

    # TODO filter to just the checkmarks for the submisions
    # in the moderator's queues.
    query = select(
        [
            arXiv_submission_flag.c.submission_id,
            arXiv_submission_flag.c.updated,
            tapir_nicknames.c.nickname,
        ]
    ).select_from(arXiv_submission_flag).join(
        tapir_nicknames,
        arXiv_submission_flag.c.user_id == tapir_nicknames.c.user_id
    )
    async with engine.connect() as conn:
        res = await conn.execute(query)
        return [{'submission_id': row[0],
                 'updated': row[1],
                 'username': row[2]} for row in res]
