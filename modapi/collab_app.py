"""Socket.IO moderator collaboration app"""

import os
import socketio
from .config import allow_origins

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=allow_origins,
    logger=bool(os.environ.get("DEBUG", False)),
    engineio_logger=bool(os.environ.get("DEBUG", False)),
)


@sio.event
async def in_edit(sid, data):
    """Items on system that are in an edit"""
    print("in_edit", data)
    await sio.emit("in_edit", data) # rebroadcast


@sio.on("join")
async def handle_join(sid, *args, **kwargs):
    await sio.emit("lobby", "User joined")


@sio.on("test")
async def test(sid, *args, **kwargs):
    await sio.emit("hey", "joe")


@sio.event
def connect(sid, env):
    print("connect ", sid, env)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)
