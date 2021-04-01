from typing import List, Optional

#from modapi.collab.collab_app import sio
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from modapi.auth import auth_user, User
from modapi.db import engine
from modapi.db.arxiv_tables import arXiv_submissions


from . import schema

router = APIRouter(
    dependencies=[Depends(auth_user)]
)


@router.get("/submissions", response_model=List[schema.Submission])
async def submissions():
 
    async with engine.connect() as conn:
        query = arXiv_submissions.select().limit(10)
        res = await conn.execute(query)
        return res.all()


@router.get("/submission/{submission_id}", response_model=schema.Submission)
async def submission(submission_id: int):
    """Gets a submission. (WIP)"""
    async with engine.connect() as conn:
        query = arXiv_submissions.select().where(
            arXiv_submissions.c.submission_id == submission_id
        )
        res = await conn.execute(query)
        return res.fetchone()
