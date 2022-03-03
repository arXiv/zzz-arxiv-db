"""Filters for submissions limited to mod's view"""
from sqlalchemy import or_, and_

from modapi.auth import User

from modapi.tables.arxiv_models import (
    Submissions,
    SubmissionCategory,
    SubmissionCategoryProposal,
)


def with_queue_filters(
    user: User,
    stmt,
    include_mod_archives: bool = True,
    exclude_mod_categories: bool = False,
    include_auto_holds: bool = False,
):
    """Returns the statement limited to just queue submissions.

    This will limit to a moderators queue if the user is a moderator.
    The filters `include_mod_archives` and `exclude_mod_categories` only
    have an effect for moderators.

    `include_auto_holds` has an effect for both mods and admins.
    """
    stmt = stmt.filter(Submissions.status.in_([1, 2, 4]))
    
    if not include_auto_holds:
        stmt = stmt.filter(Submissions.auto_hold == 0)

    if user.is_moderator and not user.is_admin:
        stmt = with_mod_filters(
            user, stmt, include_mod_archives, exclude_mod_categories
        )

    return stmt


def with_mod_filters(
    user: User,
    stmt,
    include_mod_archives: bool = True,
    exclude_mod_categories: bool = False,
):
    """Returns the stmt limited to a moderators view of the queue"""
    stmt = stmt.filter(Submissions.type.in_(["new", "rep", "cross"]))
    stmt = stmt.outerjoin(Submissions.submission_category)
    stmt = stmt.outerjoin(Submissions.proposals)

    mods_categories = user.moderated_categories

    category_ors = []

    if not (include_mod_archives and exclude_mod_categories):
        category_ors.append(SubmissionCategory.category.in_(mods_categories))
        category_ors.append(
            and_(
                SubmissionCategoryProposal.category.in_(mods_categories),
                SubmissionCategoryProposal.proposal_status == 0,
            )
        )

    if include_mod_archives:
        for archive in user.moderated_archives:
            category_ors.append(SubmissionCategory.category.startswith(archive))
            # also include proposals from moderated archives
            category_ors.append(
                and_(
                    SubmissionCategoryProposal.category.startswith(archive),
                    SubmissionCategoryProposal.proposal_status == 0,
                )
            )

        if exclude_mod_categories:
            stmt = stmt.filter(
                or_(
                    SubmissionCategory.category.not_in(mods_categories),
                    and_(
                        SubmissionCategoryProposal.category.not_in(mods_categories),
                        SubmissionCategoryProposal.proposal_status == 0,
                    ),
                )
            )

    stmt = stmt.filter(or_(*category_ors))

    return stmt
