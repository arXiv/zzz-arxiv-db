"""Caching of arXiv mod and admin users"""
from typing import Optional, Dict, List
from sqlalchemy import text
from pydantic import BaseModel

from sqlalchemy.orm import Session

from modapi.config import config

import logging
log = logging.getLogger(__name__)
if config.debug:
    log.setLevel(logging.DEBUG)


class User(BaseModel):
    """Represents an arXiv admin or mod user"""
    user_id: int
    name: str
    username: str
    is_moderator: bool = False
    is_admin: bool = False
    # pydantic handles default list correctly
    moderated_categories: List[str] = []
    moderated_archives: List[str] = []


_users: Dict[int, User] = {}


def invalidate_user(user_id: int) -> bool:
    """Remove user id from cache. Returns bool if id was in cache"""
    if user_id in _users:
        del _users[user_id]
        return True
    else:
        return False


async def getuser(user_id: int, db: Session) -> Optional[User]:
    """Gets a user by user_id"""
    if user_id in _users:
        return _users[user_id]

    user = _getfromdb(user_id, db)
    if user:
        _users[user_id] = user
        return user
    else:
        return None


async def getuser_by_nick(nick: str, db: Session) -> Optional[User]:
    by_nick = [user for user in _users.values() if user.username == nick]
    if len(by_nick) == 1:
        return by_nick[0]

    if len(by_nick) > 1:
        log.error(f"{len(by_nick)} users with the same nickname {nick[:10]}")
        return None

    user = await _getfromdb_by_nick(nick, db)
    if user:
        _users[user.user_id] = user
        return user
    else:
        return None


async def _getfromdb_by_nick(nick: str, db: Session) -> Optional[User]:
    query = """
    SELECT tapir_nicknames.user_id
    FROM tapir_nicknames
    WHERE tapir_nicknames.nickname = :nick"""

    rs = list(db.execute(text(query), {"nick": nick}))
    if not rs:
        log.debug("no user found in DB for nickname %s", nick[:10])
        return None

    return _getfromdb(rs[0]['user_id'], db)


def to_name(first_name, last_name):
    """Display name from first_name and last_name"""
    return f"{first_name} {last_name}".strip()


def _getfromdb(user_id: int, db: Session) -> Optional[User]:
    user_query = """
    SELECT 
    hex(tapir_users.first_name) as first_name,
    hex(tapir_users.last_name) as last_name,
    tapir_nicknames.nickname, tapir_users.flag_edit_users
    FROM tapir_users
    JOIN tapir_nicknames ON tapir_users.user_id = tapir_nicknames.user_id
    WHERE tapir_users.user_id = :userid"""

    # Using definitive to distinguish categories from archives
    cat_mod_query = """
    SELECT
    m.archive as 'arch', m.subject_class as 'cat', c.definitive as 'definitive'
    FROM arXiv_moderators AS m
    JOIN arXiv_categories AS c ON  m.archive = c.archive AND m.subject_class = c.subject_class
    WHERE user_id = :userid"""

    rs = list(db.execute(text(user_query), {"userid": user_id}))
    if not rs:
        return None

    mod_rs = list(db.execute(text(cat_mod_query), {"userid": user_id}))
    # normal categories like cs.LG
    cats = [f"{row['arch']}.{row['cat']}"
            for row in mod_rs if row['arch'] and row['cat']]
    # archive like categories like hep-ph
    cats.extend([row['arch'] for row in mod_rs
                 if row['arch'] and not row['cat'] and row['definitive']])
    archives = [row['arch'] for row in mod_rs
                if row['arch'] and not row['cat'] and not row['definitive']]
    ur = User(user_id=user_id,
              name=to_name(
                  bytes.fromhex(rs[0]['first_name']).decode('utf-8'),
                  bytes.fromhex(rs[0]['last_name']).decode('utf-8')),
              username=rs[0]['nickname'],
              is_admin=bool(rs[0]['flag_edit_users']),
              is_moderator=bool(cats or archives),
              moderated_categories=cats,
              moderated_archives=archives)
    log.debug("User: %s", ur)
    return ur
