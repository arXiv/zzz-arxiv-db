"""Routes for holds on submissions.

This works with the arXiv_submission_hold_reason table and is intended
to work for both mod and admin holds.

The paths in this module are intended to replace the /modhold paths.
"""
from modapi.rest.debug_log import debuglog, msg
from typing import Union, List, Optional

from sqlalchemy import select, or_, and_, null
from sqlalchemy.orm import joinedload, Session
from fastapi import APIRouter, Depends
from pydantic import conlist

from modapi.auth import User, auth_user
from modapi.db import get_db
from modapi.rest.earliest_announce import earliest_announce
from modapi.tables.arxiv_tables import (
    arXiv_admin_log,
    arXiv_submissions,
    arXiv_submission_hold_reason,
)
from modapi.tables.arxiv_models import (
    Submissions,
    SubmissionCategory,
    SubmissionCategoryProposal,
)

# TODO: not yet implemented
# from modapi.models.admin_log import comment_admin_log

from .domain import HoldReleaseLogicRes, HoldLogicRes,\
    ON_HOLD, HoldTypesIn
from .biz_logic import hold_check, release_by_mod_biz_logic, hold_biz_logic

import logging
log = logging.getLogger(__name__)

router = APIRouter()

@router.post("/submission/{submission_id}/hold")
async def hold(
        submission_id: int,
        hold: HoldTypesIn,
        user: User = Depends(auth_user),
        db: Session = Depends(get_db)
):
    """Put a submission on hold

    This will prevent it from being announced until it is released from hold.

    The sendback feature is not yet implemented.
    """
    exists = hold_check(db, submission_id)

    hold_res = hold_biz_logic(hold, exists, submission_id, user)
    if not isinstance(hold_res, HoldLogicRes):
        debuglog.debug(msg(user,
                           payload={'submission_id':submission_id, 'hold':hold},
                           status_code=hold_res.status_code))
        return hold_res

    for logtext in hold_res.modapi_comments:
        stmt = arXiv_admin_log.insert().values(
            submission_id=submission_id, paper_id=hold_res.paper_id, username=user.username,
            program="modapi.rest", command="Hold", logtext=logtext)
        res = db.execute(stmt)

    for logtext in hold_res.visible_comments:
        stmt = arXiv_admin_log.insert().values(
            submission_id=submission_id, paper_id=hold_res.paper_id, username=user.username,
            program="Admin::Queue", command="admin comment", logtext=logtext)
        res = db.execute(stmt)
        comment_id = res.lastrowid

    if hold_res.delete_hold_reason:
        db.execute(arXiv_submission_hold_reason.delete()
                   .where(arXiv_submission_hold_reason.c.submission_id == submission_id))

    if hold_res.create_hold_reason:
        stmt = arXiv_submission_hold_reason.insert().values(
            submission_id=submission_id, comment_id=comment_id, user_id=user.user_id,
            type=hold.type, reason=hold.reason)
        db.execute(stmt)

    stmt = (arXiv_submissions.update()
            .values(status=ON_HOLD)
            .where(arXiv_submissions.c.submission_id == submission_id))
    db.execute(stmt)
    db.commit()
    debuglog.debug(msg(user, payload={'submission_id':submission_id, 'hold':hold}))
    return "success"


@router.post("/submission/{submission_id}/hold/release", response_model=str)
async def hold_release(submission_id: int, user: User = Depends(auth_user),
                       db: Session = Depends(get_db)):
    """Releases a hold.

    To release a hold means to set the submission status so that it is
    available to be published.

    If Moderator the submission must be:
    - on hold
    - have a row in arXiv_submission_hold_reason

    Moderators can release any hold that has a reason in the
    arXiv_submission_hold_reason table.

    If Admin the submission must be:
    - on hold

    Admins can release holds referenced in the
    arXiv_submission_hold_reason or legacy style holds.

    """
    exists = hold_check(db, submission_id)
    release_res = release_by_mod_biz_logic(exists, submission_id, user, earliest_announce)
    if not isinstance(release_res, HoldReleaseLogicRes):
        debuglog.debug(msg(user,
                           payload={'submission_id':submission_id},
                           status_code=release_res.status_code))
        return release_res

    if release_res.clear_reason:
        db.execute(arXiv_submission_hold_reason.delete()
                   .where(arXiv_submission_hold_reason.c.submission_id == submission_id))

    # Do correct release time and stick_status
    # See arXiv::Schema::Result::Submission.propert_release_from_hold()
    sub_update=(arXiv_submissions.update()
                .values(status=release_res.release_to_status)
                .values(sticky_status=null())
                .where(arXiv_submissions.c.submission_id == submission_id))
    if release_res.set_release_time:
        sub_update.values(release_time=release_res.set_release_time)

    db.execute(sub_update)

    for logtext in release_res.modapi_comments:
        stmt = arXiv_admin_log.insert().values(
            username=user.username,
            program="modapi.rest",
            command="hold_release",
            paper_id=release_res.paper_id,
            logtext=logtext,
            submission_id=submission_id,
        )
        db.execute(stmt)

    # TODO: comment_admin_log not yet implemented
    # for logtext in release_res.visible_comments:
    #     comment_admin_log(db, user, submission_id, release_res.paper_id, logtext)
    for logtext in release_res.visible_comments:
        stmt = arXiv_admin_log.insert().values(
            username=user.username,
            program="Admin::Queue",
            command="admin comment",
            logtext=logtext,
            submission_id=submission_id,
            paper_id=release_res.paper_id
        )
        db.execute(stmt)

    db.commit()
    debuglog.debug(msg(user, payload={'submission_id':submission_id}))
    return "success"


@router.get("/holds/{submission_id}", response_model=List[conlist(Union[str, int], min_items=4, max_items=4)])
async def get_hold(
        submission_id: int,
        user: User = Depends(auth_user),
        db: Session = Depends(get_db)):
    """Gets the hold for a single submission."""
    debuglog.debug(msg(user))
    return await _holds(submission_id, user, db)


@router.get("/holds", response_model=List[conlist(Union[str, int], min_items=4, max_items=4)])
async def holds(user: User = Depends(auth_user), db: Session = Depends(get_db)):
    """Gets all existing holds.

    If the user is a moderator this only gets the holds on submissions
    of interest to the moderator.

    Returns List of [ subid, user_id, type, reason ]

    user_id, and reason may be an empty string.

    Type will be 'admin', 'mod' or 'legacy'.
    """
    debuglog.debug(msg(user))
    return await _holds(None, user, db)


async def _holds(submission_id: Optional[int], user: User, db: Session):
    query_options = [
        # Could deferre all of submission?
        joinedload(Submissions.hold_reasons),
    ]
    # TODO the admin query doesn't need any joins
    stmt = (select(Submissions)
            .outerjoin(Submissions.submission_category)
            .outerjoin(Submissions.proposals)
            .outerjoin(Submissions.hold_reasons)
            .options(*query_options)
            .filter(Submissions.status == ON_HOLD)
            )
    if user.is_moderator and not user.is_admin:
        cats = user.moderated_categories
        mod_ors = [
            SubmissionCategory.category.in_(cats),
            and_(SubmissionCategoryProposal.category.in_(cats),
                 SubmissionCategoryProposal.proposal_status == 0)
        ]
        for archive in user.moderated_archives:
            mod_ors.append(
                SubmissionCategory.category.startswith(archive))
            # modui2 excluded subs with proposals in mod's archive
            # mod_ors.append(
            #     and_(SubmissionCategoryProposal.category.startswith(archive),
            #          SubmissionCategoryProposal.proposal_status == 0))

        stmt = stmt.filter(Submissions.type.in_(['new', 'rep', 'cross']))
        stmt = stmt.filter(or_(*mod_ors))

    if submission_id is not None:
        stmt = stmt.filter(Submissions.submission_id == submission_id)

    res = db.execute(stmt)
    out = []
    for row in res.unique():
        sub = row[0]
        if sub.hold_reasons:
            out.append([int(sub.submission_id),
                        sub.hold_reasons[0].user_id,
                        sub.hold_reasons[0].type,
                        sub.hold_reasons[0].reason])
        else:
            out.append([int(sub.submission_id),
                        '', 'legacy', ''])

    return out

status_by_number = {
    0: "working",  # incomplete; not submitted
    1: "submitted",
    2: "on hold",
    3: "unused",
    4: "next",  # for tomorrow
    5: "processing",
    6: "needs_email",
    7: "published",
    8: "processing(submitting)",  # text extraction , etc
    9: "removed",
    10: "user deleted",
    19: "error state",
    # --- expired (files removed) status are the above +20, usual ones are:
    20: 'deleted(working)',  # was working but expired
    22: 'deleted(on hold)',
    25: 'deleted(processing)',
    27: 'deleted(published)',  # published and files expired
    29: "deleted(removed)",
    30: 'deleted(user deleted)'  # user deleted and files expired
}
