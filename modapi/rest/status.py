import subprocess
from pathlib import Path

from modapi.config import config
from modapi.userstore import User
from modapi.auth import auth_user
from modapi.db import get_db

from fastapi import APIRouter, HTTPException, Depends


from sqlalchemy.orm import Session
from sqlalchemy.sql import text

router = APIRouter()


@router.get("/status")
async def status(db: Session = Depends(get_db)):
    """Get the status of the ModAPI service as HTTP status code.

    Tests connection to DB. Returns an empty body on success.
    """
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=503, detail="DB is not avaiable")

    return "Good, DB up."


_GVER = None


@router.get("/version")
async def version():
    """Returns git version"""
    global _GVER
    if not _GVER:
        cmtf = Path("git-commit.txt")
        if cmtf.is_file():
            with open("git-commit.txt") as fh:
                _GVER = fh.read().rstrip()
        else:
            _GVER = subprocess.check_output(
                "git rev-parse --short HEAD".split()
            ).rstrip()

    if _GVER:
        return _GVER
    else:
        return "unknown"


@router.get("/email_log")
async def email_log(lines: int, user: User = Depends(auth_user)):
    """Gets the email debug log."""
    if not user or not user.is_admin:
        raise HTTPException(status_code=401)

    if config.email_log is None:
        return "Currently configured to not write an email."

    # Warning: getting the length and reading the log has a race
    # condition with writes to the log but not worried about it due to
    # this just being a debugging output.
    length = 0
    with open(config.email_log) as logf:
        length = len(logf.readlines())

    skip = max(length - lines, 0)
    with open(config.email_log) as logf:
        return [line for ln, line in enumerate(logf.readlines()) if ln >= skip]
