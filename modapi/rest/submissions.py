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
)

router = APIRouter()

@router.get("/submission/{submission_id}", response_model=schema.Submission)
async def submission(submission_id: int):
    """Gets a submission. (WIP)"""
    query = arXiv_submissions.select().where(
        arXiv_submissions.c.submission_id == submission_id
    )
    return await database.fetch_one(query)
