import socketio

from .rest.rest_app import fast_app
from .collab.collab_app import sio
import modapi.config as config


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Avoid taking over the fast_app root by setting the socketio_path
# socket.io client path will need to be set in the JS
socketio_path = "/ws"

app = socketio.ASGIApp(
    sio,
    fast_app,  # pass everything not handled to fast_app
    socketio_path=socketio_path,
)



if __name__ == "__main__":
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    import uvicorn

    # Don't run with reload for produciton
    uvicorn.run("modapi.app:app", host="0.0.0.0", port=8000, reload=True, debug=False)
