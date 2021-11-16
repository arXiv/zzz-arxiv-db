from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from modapi import userstore
from modapi.auth import User, auth_user
from modapi.rest.debug_log import debuglog, msg

class UserOut(BaseModel):
    username: str
    name: str
    is_moderator: bool
    is_admin: bool
    moderated_categories: List[str]
    moderated_archives: List[str]


router = APIRouter()


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(auth_user)):
    """Gets information about the currently logged in user"""
    if user and (user.is_admin or user.is_moderator):
        # Invalidate so next call will get a fresh copy of
        # the user and any updates to the user, ex. categories
        debuglog.debug(msg(user))
        userstore.invalidate_user(user.user_id)
        return user
    else:
        raise HTTPException(status_code=401)
