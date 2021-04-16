"""Publish and freeze time."""
import re
from wsgiref.handlers import format_date_time

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from modapi.auth import User, auth_user
from datetime import datetime
import requests

from pydantic import BaseModel

import logging

log = logging.getLogger(__name__)

router = APIRouter()


class Times(BaseModel):
    next: datetime
    freeze: datetime
    arxiv_tz: str


TZ_REGEX = re.compile(r'<em class="boxed">.* ([A-Z]{3}) <\/em>')


FREEZE_REGEX = re.compile(r"until the next deadline.*that is (.*UTC)")


NEXT_REGEX = re.compile(r"will be announced in the mailing.*that is (.*UTC)")


cache = Times(arxiv_tz="", next=datetime.now(), freeze=datetime.now())
# Not worying about deadlock, all chagnes are idempotent


@router.post("/times", response_model=Times)
async def hold(response: Response, user: User = Depends(auth_user)):
    """Gets times related operation of the submission system."""

    now = datetime.now()
    if now >= cache.freeze or now >= cache.next or cache.arxiv_tz is "":
        resp = requests.request(
            method="GET", url="https://arxiv.org/localtime", stream=True
        )
        if resp.status_code != 200:
            return JSONResponse(
                status_code=502,
                content={
                    "msg": f"failed to get arxiv.org localtime {resp.status_code}"
                },
            )

        tz, nxt, freeze = (None, None, None)
        for line in resp.iter_lines(decode_unicode=True):
            log.error(line)
            if not line:
                continue
            if not tz:
                mtc = TZ_REGEX.search(line)
                if mtc:
                    tz = mtc.group(1)
            if not freeze:
                mtc = FREEZE_REGEX.search(line)
                if mtc:
                    freeze = mtc.group(1)
            if not nxt:
                mtc = NEXT_REGEX.search(line)
                if mtc:
                    nxt = mtc.group(1)
            if tz and nxt and freeze:
                break

        fmt_1123 = "%a, %d %b %Y %H:%M %Z"

        cache.freeze = datetime.strptime(freeze, fmt_1123)
        cache.next = datetime.strptime(nxt, fmt_1123)
        cache.arxiv_tz = tz

    response.headers["Expires"] = format_date_time(
        min([cache.next, cache.freeze]).timestamp()
    )
    return cache
