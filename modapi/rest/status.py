import subprocess
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends

from modapi.db import get_db

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
        raise HTTPException(status_code=503, detail='DB is not avaiable')

    return 'Good, DB up.'


_GVER = None


@router.get("/version")
async def version():
    """Returns git version"""
    global _GVER
    if not _GVER:
        cmtf = Path('git-commit.txt')
        if cmtf.is_file():
            with open('git-commit.txt') as fh:
                _GVER = fh.read().rstrip()
        else:
            _GVER = subprocess.check_output('git rev-parse --short HEAD'.split()).rstrip()

    if _GVER:
        return _GVER
    else:
        return "unknown"
