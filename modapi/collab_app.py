"""Socket.IO moderator collaboration app

Soft lock 

To listen to locks and unlocks subscribe to lock and unlock.

To  lock:

emit lock {id: 1234, user: bob}

To unlock:

emit unlock {id: 1234, user: bob}
"""

import socketio
from .config import allow_origins, debug

    
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=allow_origins,
    logger=debug,
    engineio_logger=debug,
)


@sio.event
async def lock(sid, *args, **kwargs):
    # TODO validate data
    # TODO save lock
    await sio.emit("lock", args)


@sio.event
async def unlock(sid, *args, **kwargs):
    # TODO validate data
    # TODO Remove lock from store
    await sio.emit("unlock", args)


@sio.event
async def connect(sid, env):
    sio.logger.error(f"{__file__} CONNECTED {sid}")
    sio.logger.error(f"{__file__} ENV IS: {env}")


@sio.event
async def disconnect(sid):
    # TODO unlock all held by this sid
    print("disconnect ", sid)
