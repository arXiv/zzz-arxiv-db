"""Caching of arXiv mod and admin users"""
from typing import Optional, Dict, List, Tuple
from sqlalchemy import text
from pydantic import BaseModel

from sqlalchemy.orm import Session

from arxiv.taxonomy.definitions import ARCHIVES_ACTIVE, CATEGORIES, CATEGORIES_ACTIVE

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

    def can_edit_category(self, category:str) -> bool:
        return (category in CATEGORIES and (
            self.is_admin or
            category in self.moderated_categories or
            any([cat for cat in self.moderated_categories
                 if CATEGORIES[cat]['in_archive'] in self.moderated_archives])
        ))

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

    rs = list(db.execute(text(user_query), {"userid": user_id}))
    if not rs:
        return None

    cats, archives = _cats_and_archives(user_id, db)
    ur = User(user_id=user_id,
              name=to_name(
                  bytes.fromhex(rs[0]['first_name']).decode('utf-8'),
                  bytes.fromhex(rs[0]['last_name']).decode('utf-8')),
              username=rs[0]['nickname'],
              is_admin=bool(rs[0]['flag_edit_users']),
              is_moderator=bool(cats or archives),
              moderated_categories=cats,
              moderated_archives=archives)
    return ur

def _cats_and_archives(user_id: int, db: Session) -> Tuple[List[str],List[str]]:
    """Archives and categories for the moderator.

    Returns
    -------
    Tuple of (categories, archives)

    The archvies list can be thought of as a lit of things that have sub-categories
    The categories list can be thought of as a list of things that have submissions.
    """
    cat_mod_query = """SELECT archive as 'arch', subject_class as 'cat'
    FROM arXiv_moderators WHERE user_id = :userid"""
    mod_rs = list(db.execute(text(cat_mod_query), {"userid": user_id}))

    archives = [row['arch'] for row in mod_rs
                if row['arch'] and not row['cat'] and row['arch'] in ARCHIVES_ACTIVE]

    # normal categories like cs.LG
    cats = [f"{row['arch']}.{row['cat']}"
            for row in mod_rs if row['arch'] and row['cat']]

    # Archive like categories. ex. hep-ph, gr-qc, nucl-ex, etc.
    # Don't include inactive archives since they should have been
    # subsumed (ex cmp-lg -> cs.LG) or turned to archives (ex cond-mat).
    cats.extend([row['arch'] for row in mod_rs
                 if row['arch'] and not row['cat']
                 and row['arch'] in CATEGORIES_ACTIVE])
    return (cats, archives)
