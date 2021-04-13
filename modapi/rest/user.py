from typing import List

from fastapi import APIRouter, Depends, HTTPException
from modapi.auth import User, auth_user
from pydantic import BaseModel


class UserOut(BaseModel):
    username: str
    is_mod: bool
    is_admin: bool
    categories: List[str]
    archives: List[str]


router = APIRouter()


@router.get("/me", response_model=UserOut)
async def me(user: User = Depends(auth_user)):
    """Gets information about the currently logged in user"""
    if user and (user.is_admin or user.is_mod):
        return user
    else:
        raise HTTPException(status_code=401)
