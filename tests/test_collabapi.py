"""Test of collab_app"""


from typing import List, Optional
# stdlib imports
import asyncio

# 3rd party imports
import pytest
import socketio
import uvicorn

# FastAPI imports
from fastapi import FastAPI

from .uivcorn_test_server import UvicornTestServer


PORT = 8000
IP = '127.0.0.1'

from modapi import __version__

from modapi.app import app


def test_version():
    assert __version__ == "0.1.0"

# deactivate monitoring task in python-socketio to avoid errores during shutdown
#app.eio.start_service_task = False


@pytest.fixture
async def startup_and_shutdown_server():
    """Start server as test fixture and tear down after test"""
    server = UvicornTestServer(app,IP,PORT)
    await server.up()
    yield
    await server.down()


@pytest.mark.asyncio
async def test_collab_simple(startup_and_shutdown_server):
    """A simple websocket test"""

    sio = socketio.AsyncClient()
    future = asyncio.get_running_loop().create_future()

    expected = "connected"
    @sio.event
    def connect():
        # set the result
        future.set_result(expected)

    await sio.connect(f'http://{IP}:{PORT}', socketio_path='/ws/socket.io/')

    # await sio.emit('chat message', message)
    # wait for the result to be set (avoid waiting forever)
    await asyncio.wait_for(future, timeout=1.0)
    await sio.disconnect()
    assert future.result() == expected

        
