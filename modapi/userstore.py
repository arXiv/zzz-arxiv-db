"""Caching of arXiv mod and admin users"""
from pprint import pformat

from typing import Optional, Dict, List

from sqlalchemy import text

import modapi.db as db

from modapi.db.arxiv_tables import tapir_nicknames, tapir_users, arXiv_moderators

from pydantic import BaseModel

import logging
log = logging.getLogger(__name__)


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


async def getuser_by_nick(nick: str) -> Optional[User]:
    by_nick = [user for user in _users.items() if user.username == nick]
    if len(by_nick) == 1:
        return by_nick[0]

    if len(by_nick) > 1:
        log.error(f"{len(by_nick)} users with the same nickname {nick[:10]}")
        return None

    user = await _getfromdb_by_nick(nick)

    if user:
        _users[user.user_id] = user
        return user
    else:
        return None


async def _getfromdb_by_nick(nick: str) -> Optional[User]:
    query = """
    SELECT tapir_nicknames.user_id
    FROM tapir_nicknames
    WHERE tapir_nicknames.nickname = :nick"""

    async with db.engine.begin() as conn:
        rs = list(await conn.execute(text(query), {"nick": nick}))
        if not rs:
            log.debug("no user found in DB for nickname %s", nick[:10])
            return None

        return await _getfromdb(rs[0]['user_id'])


async def _getfromdb(user_id: int) -> Optional[User]:
    query = """SELECT tapir_nicknames.nickname, tapir_users.flag_edit_users, arXiv_moderators.archive, arXiv_moderators.subject_class 
    FROM tapir_users
    JOIN tapir_nicknames ON tapir_users.user_id = tapir_nicknames.user_id
    LEFT JOIN arXiv_moderators ON tapir_users.user_id = arXiv_moderators.user_id
    WHERE tapir_users.user_id = :userid"""

    async with db.engine.begin() as conn:
        rs = list(await conn.execute(text(query), {"userid": user_id}))
        if not rs:
            return None

        if log.isEnabledFor(logging.DEBUG):
            log.debug("userstore result: %s", pformat(rs))

        cats = [f"{row[2]}.{row[3]}"
                for row in rs if row[2] and row[3]]
        archives = [row[2] for row in rs if row[2] and not row[3]]

        values = {
            'user_id': user_id,
            'username': rs[0]['nickname'],
            'is_admin': bool(rs[0]['flag_edit_users']),
            'is_mod': bool(cats or archives),
            'categories': cats,
            'archives':  archives
        }

        return User(**values)
