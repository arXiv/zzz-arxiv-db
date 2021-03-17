"""Caching of arXiv mod and admin users"""
from typing import Optional, Dict, List

from sqlalchemy.sql import select

import modapi.db as db

from modapi.db.arxiv_tables import tapir_nicknames, tapir_users, arXiv_moderators

from pydantic import BaseModel


class User(BaseModel):
    """Represents an arXiv admin or mod user"""
    user_id: int
    username: str
    is_mod: bool = False
    is_admin: bool = False
    categories: List[str] = [] # pydantic handles default list correctly
    archives: List[str] = []


_users: Dict[int, User] = {}



async def getuser(user_id: int) -> Optional[User]:
    """Gets a user by user_id"""
    

    
    if user_id in _users:
        return _users[user_id]
    
    user = await _getfromdb(user_id)
    if user:
        _users[user_id] = user
        return user
    else:
        return None


async def _getfromdb(user_id: int) -> Optional[User]:
   
    query = """SELECT tapir_nicknames.nickname, tapir_users.flag_edit_users, arXiv_moderators.archive, arXiv_moderators.subject_class 
    FROM tapir_users
    JOIN tapir_nicknames ON tapir_users.user_id = tapir_nicknames.user_id
    LEFT JOIN arXiv_moderators ON tapir_users.user_id = arXiv_moderators.user_id
    WHERE tapir_users.user_id = :userid"""

    
    rs = list(await db.database.fetch_all(query, {"userid": user_id}))
    if not rs:
        return None

    values = {
        'user_id': user_id,
        'username':rs[0]['nickname'],
        'is_admin': rs[0]['flag_edit_users'],
        'is_mod': any(('archive' in row or 'subject_class' in row for row in rs)),
        'categories': [f"{row['archive']}.{row['subject_class']}" for row in rs if 'archive' in row and 'subject_class' in row and row['archive'] and row['subject_class']],
        'archives':  [row['archive'] for row in rs if 'archive' in row and 'subject_class' not in row],
        }

    return User(**values)
