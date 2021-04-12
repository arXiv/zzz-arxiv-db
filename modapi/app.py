import socketio

from .rest.rest_app import fast_app
from .collab.collab_app import sio
import modapi.config as config

# Avoid taking over the fast_app root by setting the socketio_path
# socket.io client path will need to be set in the JS
socketio_path = "/ws"


app = socketio.ASGIApp(
    sio,
    fast_app,  # pass everything not handled to fast_app
    socketio_path=socketio_path,
)


def run_app(reload, uvicorn_debug, log_debug):
    """Run the modAPI app.
    
    reload: If true, reload the app on any code changes saved to disk. Don't
    use this in production. 

    uvicorn_debug: output debugging messages from uvicorn. Avoid using
    this in produciton.

    log_debug: Set log level to debug and output SQLAlchemy debugging. Avoid using
    this in produciton.

    """
    import logging
    import sys

    if log_debug:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    import uvicorn

    # Don't run with reload for produciton
    uvicorn.run("modapi.app:app", host="0.0.0.0", port=8000, reload=reload, debug=uvicorn_debug)
    

if __name__ == "__main__":
    run_app(config.reload, config.uvicorn_debug, config.debug)
