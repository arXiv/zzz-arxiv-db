"""Storage of soft locks on submissions
"""
from asyncio import Semaphore
from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class Lock():
    username: str
    sid: int
    def copy(self):
        return Lock(**self.__dict__)

_locks: Dict[int, Lock] = {}
"""A dict of locked submission ids.

Must aquire semaphore before using this"""

# TODO Since single thread operation is needed for uvicorn when doing
# socket.io, a semaphore might not be needed.  Each async function
# should run to completion without interuption so they define the
# whole "happens before" semantics.  OTOH it should cause little
# overhead if it is never waits.

_semaphore = Semaphore()
"""Semaphore for both locks and users"""


async def lock(sub_id, sid, username):
    async with _semaphore:
        if sub_id in _locks:
            return f"Id {sub_id} already locked"
        else:
            _locks[sub_id] = Lock(username=username, sid=sid)
            return None


async def unlock(sub_id, sid, username):
    async with _semaphore:
        if sub_id not in _locks:
            return f"Id {sub_id} not locked"
        elif sid != _locks[sub_id].sid and username != _locks[sub_id].username:
            return f"Id is not locked by either {sid} or {username}"
        else:
            del _locks[sub_id]
            return None


async def unlock_for_sid(sid):
    """Unlock all locks for a sid.

    Returns list of submission ids unlocked."""
    async with _semaphore:
        deleted = []
        for sub_id, lok in list(_locks.items()):
            if lok.sid == sid:
                deleted.append(sub_id)
                del _locks[sub_id]

        return deleted


async def current_locks():
    async with _semaphore:
        return _locks.copy()


async def is_locked(sid) -> Optional[Lock]:
    async with _semaphore:
        if sid in _locks:
            return _locks[sid].copy()
        else:
            return None
