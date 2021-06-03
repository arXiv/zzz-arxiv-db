"""Filters for submissions limited to mod's view"""
from sqlalchemy import or_, and_

from modapi.auth import User

from modapi.tables.arxiv_models import (
    Submissions,
    TapirUsers,
    Demographics,
    CategoryDef,
    SubmissionCategory,
    SubmissionCategoryProposal,
    AdminLog,
)


def with_queue_filters(user: User, stmt):
    """Returns the statement limited to just queue submissions.

    This will limit to a moderators queue is user is a moderator."""
    stmt = stmt.filter(Submissions.status.in_([1, 2, 4]))
    if user.is_moderator and not user.is_admin:
        stmt = with_mod_filters(user, stmt)

    return stmt


def with_mod_filters(user: User, stmt):
    """Returns the stmt limited to a moderators view of the queue"""
    stmt = stmt.filter(Submissions.type.in_(['new', 'rep', 'cross']))
    stmt = stmt.outerjoin(Submissions.submission_category)
    stmt = stmt.outerjoin(Submissions.proposals)
    mods_categories = user.moderated_categories
    category_ors = [
        SubmissionCategory.category.in_(mods_categories),
        and_(
            SubmissionCategoryProposal.category.in_(mods_categories),
            SubmissionCategoryProposal.proposal_status == 0,
        ),
    ]
    for archive in user.moderated_archives:
        category_ors.append(
            SubmissionCategory.category.startswith(archive))
        
    stmt = stmt.filter(or_(*category_ors))
    return stmt

