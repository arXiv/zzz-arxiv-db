"""Socket.IO moderator collaboration app

Soft lock 

To listen to locks and unlocks subscribe to lock and unlock.

To  lock:

emit lock {id: 1234, username: bob}

To unlock:

emit unlock {id: 1234}
"""
from asyncio import gather
from typing import List

import socketio

import modapi.collab.lockstore as lockstore
from modapi.config import allow_origins, debug


sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=allow_origins,
    logger=debug,
    engineio_logger=debug,
)


def _validate_id(data):
    err = []
    if not data:
        err.append("no data")
    if "id" not in data:
        err.append("lacks id")
    if "id" in data and not isinstance(data["id"], int):
        err.append("id is not an int")

    return err


def _validate_id_and_user(data):
    err = _validate_id(data)
    if "username" not in data:
        err.append("lacks user")
    if "username" in data and not isinstance(data["username"], str):
        err.append("user is not a str")
    return err


@sio.event
async def lock(sid, data):
    err = _validate_id_and_user(data)
    if err:
        emsg = ", ".join(err)
        await sio.emit("errors", f"Error on lock, {emsg}", to=sid)
        sio.logger.error(f"Error with lock from {sid}: {emsg}")
        return

    user = data["username"]
    id = data["id"]

    err = await lockstore.lock(id, sid, user)
    if err:
        await sio.emit("errors", f"Error while locking: {err} ", to=sid)
        return
    else:
        await sio.emit("lock", {"id": id, "username": user})


@sio.event
async def unlock(sid, data):
    sio.logger.error(data)
    err = _validate_id(data)
    if err:
        emsg = ", ".join(err)
        await sio.emit("errors", f"Error on unlock, {emsg}", to=sid)
        sio.logger.error(f"Error with unlock from {sid}: {emsg}")
        return

    id = data["id"]

    err = await lockstore.unlock(id, sid, None)
    if err:
        await sio.emit("errors", f"Error while unlocking: {err}", to=sid)
        return
    else:
        await _unlock(id)


@sio.event
async def refresh(sid, data):
    """Useful for a client to request current locks"""
    current_locks = await lockstore.current_locks()

    sio.logger.error(current_locks)
    for id, lck in current_locks.items():
        await sio.emit("lock", {"id": id, "username": lck.username}, to=sid)


@sio.event
async def connect(sid, env):
    sio.logger.error(f"{__file__} CONNECTED {sid}")
    # sio.logger.error(f"{__file__} ENV IS: {env}")


@sio.event
async def disconnect(sid):
    to_unlock = await lockstore.unlock_for_sid(sid)
    await _send_unlocks(to_unlock)

    sio.logger.error(f"disconnect {sid} and unlocked {len(to_unlock)}")


async def _send_unlocks(to_unlock: List[int]):
    """Send a list of unlocks in parallel"""
    tasks = [_unlock(id) for id in to_unlock]
    await gather(*tasks)


async def _unlock(id: int):
    """Emit unlock a single paper id"""
    await sio.emit("unlock", {"id": id})
