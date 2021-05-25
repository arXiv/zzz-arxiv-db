"""ModAPI2 earliest_announce

The publish time info and holiday schedule are encoded in the Perl
libraries.  That is needed to figure out the earliest announcement
date for a submission. The earliest announcement date is needed to do
proper handling of times on a submission during a release from hold to
figure out of release_time needs to be set. That affects the paper ID
of a submission at publish time. The idea is that the paper id
assignment should be fair to the submitters with earlier submissions
getting lower number IDs.

Why not just do have the info need for this in python?

Answer: We don't want two sources of data for holidays."""

from typing import Union
import modapi.config as config
from datetime import datetime

import requests
from http import cookiejar

_req_sess = None


def _session():
    """Gets requests session that is reused for all threads.

    Consider using threading.local if this causes problems."""
    global _req_sess
    if not _req_sess:
        class BlockAll(cookiejar.CookiePolicy):
            return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, * \
                args, **kwargs: False
            netscape = True
            rfc2965 = hide_cookie2 = False
        _req_sess = requests.Session()
        _req_sess.cookies.set_policy(BlockAll())

    return _req_sess


async def earliest_announce(sub_id: int) -> Union[datetime, int]:
    """Earliest announcement that a submission could appear in

    Returns datetime if successful or an HTTP status if unsuccessful.
    """
    with _session().get('{config.earliest_announce_url}/{sub_id}') as resp:
        if resp.status_code == 200:
            return resp.json()[0]
        else:
            return resp.status_code
