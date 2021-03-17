from typing import List, Optional

#from modapi.collab.collab_app import sio
import modapi.config as config
from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi import status as httpstatus
from fastapi.responses import JSONResponse
from modapi.auth import auth
from modapi.db import database, engine
from modapi.db.arxiv_tables import arXiv_submissions
from sqlalchemy.sql import and_, select

from . import schema

router = APIRouter()

@router.get("/submissions", response_model=List[schema.Submission])
async def submissions():
    query = arXiv_submissions.select()
    return await database.fetch_all(query)


    
@router.get("/submission/{submission_id}", response_model=schema.Submission)
async def submission(submission_id: int):
    """Gets a submission. (WIP)"""
    query = arXiv_submissions.select().where(
        arXiv_submissions.c.submission_id == submission_id
    )
    return await database.fetch_one(query)
