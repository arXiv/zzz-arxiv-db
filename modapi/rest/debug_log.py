import logging
import json

from fastapi import APIRouter, Depends, HTTPException

from modapi.userstore import User
from modapi.auth import auth_user

debuglog = logging.getLogger(__file__)
debuglog.setLevel(logging.DEBUG)

filename = "debug.log"

file_handler = logging.FileHandler(filename, mode="a")


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(
            {
                "time": self.formatTime(record, self.datefmt),
                "func": record.funcName,
                "file": record.pathname,
                "msg": record.getMessage(),
            }
        )


file_handler.setFormatter(JsonFormatter())


def filter_msgs(record):
    return __file__ == record.name


file_handler.addFilter(filter_msgs)
debuglog.addHandler(file_handler)
debuglog.propagate = False
router = APIRouter()


def msg(user, payload=None, status_code=200, err_msg=None):
    data= {"user": user, "payload": payload, "status_code": status_code}
    if err_msg:
        data['err_msg']=err_msg

    return data


@router.get("/debug_log")
async def debug_log(lines: int = 10000, user: User = Depends(auth_user)):
    """Gets the debugging log."""
    if not user or not user.is_admin:
        return HTTPException(status_code=401, detail='Unauthorized dl_dl')

    # Warning: getting the length and reading the file has a race
    # condition with writes but not worried about it due to this just
    # being a debugging output.
    length = 0 
    with open(filename) as logf:
        length = len(logf.readlines())

    skip = max(length - lines, 0)
    with open(filename) as logf:
        return [json.loads(line) for ln, line in enumerate(logf.readlines()) if ln >= skip]
        
