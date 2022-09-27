"""Publish and freeze time."""
import logging
from datetime import datetime, timezone
import requests

from wsgiref.handlers import format_date_time

from pydantic import BaseModel
from fastapi import APIRouter, Response,  HTTPException

from modapi.config import config

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


def _get_timepage():
    resp = requests.request(
        method="GET", url=config.time_url,
        headers={'Accept': 'application/json'}
    )
    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            content={"msg": f"failed to get {config.time_url} status: {resp.status_code}"})

    return resp


def parse_time(time: str) -> datetime:
    return datetime.fromisoformat(time)


def _get_times(resp):
    try:
        data = resp.json()
        return Times(next_mail=parse_time(data["next_mail"]),
                     next_freeze=parse_time(data["next_freeze"]),
                     subsequent_mail=parse_time(data["subsequent_mail"]),
                     arxiv_tz=data["arxiv_tz"])
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=502,
                            content={"msg":f"Failed to parse response from {config.time_url}"})


def get_arxiv_times() -> Times:
    """Gets the next_mail and next_freeze times from `config.time_url"""
    now = datetime.now(timezone.utc).astimezone()
    if now >= cache.next_freeze or now >= cache.next_mail or cache.arxiv_tz == "":
        times = _get_times(_get_timepage())
        cache.arxiv_tz = times.arxiv_tz
        cache.next_mail = times.next_mail
        cache.next_freeze = times.next_freeze
        cache.subsequent_mail = times.subsequent_mail

    return cache

def is_freeze() -> bool:
    """Gets if the freeze is in effect.

    Sinces this uses `get_arxiv_times()` which gets the times from
    arXiv.org, this handles holidays.
    """
    times =  get_arxiv_times()
    return times.next_freeze > times.next_mail


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
    times = get_arxiv_times()
    response.headers["Expires"] = format_date_time(
        min([times.next_mail, times.next_freeze]).timestamp()
    )
    return times
