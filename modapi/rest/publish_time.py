"""Publish and freeze time."""

from wsgiref.handlers import format_date_time

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from modapi.auth import User, auth_user
from modapi.config import time_url
from datetime import datetime, timezone
import requests

from pydantic import BaseModel

import logging

log = logging.getLogger(__name__)

router = APIRouter()


class Times(BaseModel):
    next_mail: datetime
    next_freeze: datetime
    subsequent_mail: datetime
    arxiv_tz: str


cache = Times(arxiv_tz="",
              next_mail=datetime.now(timezone.utc),
              next_freeze=datetime.now(timezone.utc),
              subsequent_mail=datetime.now(timezone.utc))
# Not worying about deadlock, all chagnes are idempotent


def get_timepage():
    resp = requests.request(
        method="GET", url=time_url,
        headers={'Accept': 'application/json'}
    )
    if resp.status_code != 200:
        return JSONResponse(
            status_code=502,
            content={
                "msg": f"failed to get arxiv.org localtime {resp.status_code}"
            },
        )
    return resp


def parse_time(time: str) -> datetime:
    return datetime.fromisoformat(time)


def get_times(resp):
    try:
        data = resp.json()
        return Times(next_mail=parse_time(data["next_mail"]),
                     next_freeze=parse_time(data["next_freeze"]),
                     subsequent_mail=parse_time(data["subsequent_mail"]),
                     arxiv_tz=data["arxiv_tz"])
    except Exception as e:
        log.error(e)
        return JSONResponse(status_code=502,
                            content={"msg":f"Failed to parse response from {time_url}"})


@router.get("/times", response_model=Times)
async def times(response: Response):
    """Gets times related operation of the submission system.
    
    arxiv_tz: The timezone of the arXiv business offices. This is not
    the timezone of the times in the response. Those should be in UTC.

    next_mail: The date and time of the next announcement mailing.

    next_freeze: The date and time of the next submission
    deadline. This may be earlier than next_mail, meaning that the
    current time is before the deadline to get in the next_mail
    announcement. Or it may be after next_mail, meaning that the
    current time is later than the deadline to get in the next_mail
    announcement.

    subsequent_mail: The date and time of the announcement mailing
    that is after next_mail. If the current time is after deadline for
    next_mail, articles submitted before next_freeze are scheduled to
    be announced in this mailing.

    Articles may be held and delayed due to moderation or technical
    reasons.

    """
    now = datetime.now(timezone.utc).astimezone()
    if now >= cache.next_freeze or now >= cache.next_mail or cache.arxiv_tz == "":
        obj = get_timepage()
        if(isinstance(obj, JSONResponse)):
            return obj

        times = get_times(obj)
        if(isinstance(times, JSONResponse)):
            return times

        cache.arxiv_tz = times.arxiv_tz
        cache.next_mail = times.next_mail
        cache.next_freeze = times.next_freeze
        cache.subsequent_mail = times.subsequent_mail

    response.headers["Expires"] = format_date_time(
        min([cache.next_mail, cache.next_freeze]).timestamp()
    )
    return cache
