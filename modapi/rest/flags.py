from typing import List, Optional

# from modapi.collab.collab_app import sio
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from modapi.db import database
from modapi.db.arxiv_tables import (
    arXiv_submission_mod_flag
)
from sqlalchemy.sql import and_, select
from sqlalchemy import exc

from . import schema

router = APIRouter()


@router.put("/submission/{submission_id}/flag")
async def put_flag(submission_id: int, flag: schema.ModFlag):
    # TODO validate user


    try:
        stmt = arXiv_submission_mod_flag.insert().values(
            username=flag.username,
            flag=schema.modflag_to_int[flag.flag],
            submission_id=submission_id,
        )
        await database.execute(stmt)
    except exc.IntegrityError:
        return JSONResponse(
            status_code=409,
            content={"msg": "Flag already exists"})


@router.post("/submission/{submission_id}/flag/delete")
async def del_flag(submission_id: int, flag: schema.ModFlagDel):
    # validate user

    # TODO check that user owns the flag

    await database.execute(
        arXiv_submission_mod_flag.delete().where(
            and_(
                arXiv_submission_mod_flag.c.submission_id == submission_id,
                arXiv_submission_mod_flag.c.username == flag.username,
            )
        )
    )


@router.get("/flags", response_model=List[schema.ModFlagOut])
async def modflags():
    """Gets list of submissions with checkmarks"""
    # TODO check the user

    # TODO filter to just the checkmarks for the submisions
    # in the moderator's queues.
    query = select(
        [
            arXiv_submission_mod_flag.c.submission_id,
            arXiv_submission_mod_flag.c.updated,
            arXiv_submission_mod_flag.c.username,
        ]
    ).select_from(arXiv_submission_mod_flag)

    return await database.fetch_all(query)
