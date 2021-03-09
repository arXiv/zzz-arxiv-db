from typing import List, Optional

from fastapi import APIRouter

from fastapi import HTTPException, Cookie, Depends
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse

from sqlalchemy.sql import select, and_

#from modapi.collab.collab_app import sio
import modapi.config as config

from modapi.db import database, engine

from modapi.auth import auth

from . import schema

from modapi.db.arxiv_tables import (
    arXiv_submissions,
    arXiv_submission_mod_hold,
    arXiv_admin_log,
    arXiv_submission_mod_flag,
    tapir_nicknames,
    submission_mod_flag_create
)

router = APIRouter()


@router.put("/submission/{submission_id}/flag")
async def put_flag(submission_id: int, flag: schema.ModFlag):
    # TODO validate user

    # TODO handle duplicate entry better, right now it is a 500
    # due to a pymysql.err.IntegrityError. Do a 409
    stmt = arXiv_submission_mod_flag.insert().values(
        username=flag.username,
        flag=schema.modflag_to_int[flag.flag],
        submission_id=submission_id,
    )
    await database.execute(stmt)


@router.post("/submission/{submission_id}/flag/delete")
async def del_flag(submission_id: int, flag: schema.ModFlagDel):
    # validate user

    # TODO check that user owns the flag

    await database.execute(
        arXiv_submission_mod_flag.delete()
        .where( and_(arXiv_submission_mod_flag.c.submission_id == submission_id,
                     arXiv_submission_mod_flag.c.username == flag.username ))
    )
    

@router.get("/flags", response_model=List[schema.ModFlagOut])
async def modflags():
    """Gets list of submissions with checkmarks"""
    # TODO check the user
    
    # TODO filter to just the checkmarks for the submisions
    # in the moderator's queues.
    query = select(
        [arXiv_submission_mod_flag.c.submission_id,
         arXiv_submission_mod_flag.c.updated,
         arXiv_submission_mod_flag.c.username]
    ).select_from(arXiv_submission_mod_flag)                  

    return await database.fetch_all(query)


