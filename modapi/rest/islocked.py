"""Routes for is_edit_locked on submissions."""
from typing import Union, Literal

from fastapi import APIRouter, Depends

from modapi.auth import User, auth_user
from modapi.collab.lockstore import is_locked as check_if_locked

from pydantic import BaseModel

import logging
log = logging.getLogger(__name__)

router = APIRouter()


class Locked(BaseModel):
    """"Is the submission edit locked or not"""
    is_locked: Literal[True]
    username: str


class NotLocked(BaseModel):
    """The submission is not locked"""
    is_locked: Literal[False]


LockedOrNot = Union[Locked, NotLocked]


@router.get("/submission/{submission_id}/is_locked",
            response_model=LockedOrNot)
async def is_locked(submission_id: int, user: User = Depends(auth_user)):
    """Checks if the submission is locked for editing.

    Note, this is just advisory locking for editing in the arxiv-check
    UI. This is not the admin lock that blocks all chagnes to the
    submission.

    Note, that doesn't return a 404 if the submission does not exist.
    """
    locked = await check_if_locked(submission_id)    
    if locked:
        return Locked(is_locked=True, username=locked.username)
    else:
        return NotLocked(is_locked=False)
