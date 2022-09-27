"""Module for monitoring changes to submission in the classic arXiv DB"""

from typing import Callable, Tuple, List, Any
from sqlalchemy import select
import asyncio

from modapi.tables.arxiv_models import AdminLog

import logging

log = logging.getLogger(__name__)

CHECK_PERIOD_SECONDS = 5
"""How frequently to query the DB for changes"""

COLD_CHECK_NUM_SUBS = 20
"""Number of latest submissions to return on a cold start.

Must be greater than 0."""

Changes = Tuple[int, List[Tuple[int, str]]]
"""Chnages from the check for chagnes.

The int is the largest admin_log key from the latest check.

The list of Tuples is the [submission_id, change_area].

Change area is not yet defined but is liley to be be things like
"data", "hold", "proposals", "category". These are intended to be
useful by the UI in case there would be different endpoints that would
be needed to get the updated data.
"""


def _area_for_row(row) -> str:
    """Gets a change type for a row"""
    # TODO This should check the arXiv_admin_log row and send some
    # additinal info about the change event. The UI probably needs to
    # get information about queue changes, submisison added, submission removed,
    # submission published, flag changes, holds and releases.
    return ''


async def _check_for_changes(get_db, latest: int) -> Changes:
    """Check the DB for changes a single time.

    Sessions is the SQLAlchemy sessionmaker.

    latest is the latest arXiv_admin_log.id from the previous check.
    """
    db_gen = get_db()
    db = next(db_gen)
    try:
        stmt = select(AdminLog)
        if latest > 0:
            log.debug("Checking for admin_log ids greater than %d", latest)
            stmt = stmt.where(AdminLog.id > latest)
        else:
            # On cold start the query needs to returns something
            # so the new_latest can be populated
            log.debug("Cold start of check_for_changes: doing %d", COLD_CHECK_NUM_SUBS)
            stmt = stmt.limit(COLD_CHECK_NUM_SUBS).order_by(AdminLog.id.desc())

        rows = db.execute(stmt).scalars().all()
        if not rows:
            return [latest, []]
        else:
            new_latest = max([row.id for row in rows])
            log.debug("setting new_latest to %d", new_latest)
            return [new_latest, set([(row.submission_id, _area_for_row(row)) for row in rows])]
    finally:
        db.close()


async def periodic_check(get_db,
                         callback: Callable[[Changes], Any]):
    latest = -1
    while True:
        try:
            await asyncio.sleep(CHECK_PERIOD_SECONDS)
            latest, changes = await _check_for_changes(get_db, latest)
            await callback(latest, changes)
        except Exception:
            logging.exception("Exception in periodic_check")

